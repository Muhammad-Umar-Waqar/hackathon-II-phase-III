"""
Performance optimization utilities for the Todo application
"""
from functools import lru_cache
from typing import Optional
import time


class PerformanceMonitor:
    """Monitor and log performance metrics"""

    def __init__(self):
        self.metrics = {}

    def record_metric(self, operation: str, duration: float):
        """Record a performance metric"""
        if operation not in self.metrics:
            self.metrics[operation] = {
                'count': 0,
                'total_time': 0,
                'min_time': float('inf'),
                'max_time': 0
            }

        self.metrics[operation]['count'] += 1
        self.metrics[operation]['total_time'] += duration
        self.metrics[operation]['min_time'] = min(self.metrics[operation]['min_time'], duration)
        self.metrics[operation]['max_time'] = max(self.metrics[operation]['max_time'], duration)

    def get_metrics(self, operation: Optional[str] = None):
        """Get performance metrics"""
        if operation:
            if operation in self.metrics:
                metric = self.metrics[operation]
                return {
                    'operation': operation,
                    'count': metric['count'],
                    'avg_time': metric['total_time'] / metric['count'],
                    'min_time': metric['min_time'],
                    'max_time': metric['max_time']
                }
            return None

        return {
            op: {
                'count': m['count'],
                'avg_time': m['total_time'] / m['count'],
                'min_time': m['min_time'],
                'max_time': m['max_time']
            }
            for op, m in self.metrics.items()
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def measure_performance(operation_name: str):
    """Decorator to measure function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            performance_monitor.record_metric(operation_name, duration)

            # Log slow operations (> 1 second)
            if duration > 1.0:
                from ..utils.logger import logger
                logger.warning(f"Slow operation detected: {operation_name} took {duration:.3f}s")

            return result
        return wrapper
    return decorator


@lru_cache(maxsize=128)
def cache_user_lookup(user_id: int):
    """Cache user lookups to reduce database queries"""
    # This is a placeholder - actual implementation would query the database
    # The LRU cache will store the most recent 128 user lookups
    pass


class QueryOptimizer:
    """Optimize database queries"""

    @staticmethod
    def get_optimized_task_query(db, user_id: int, filters: dict = None):
        """
        Get optimized task query with eager loading
        """
        from ..models.task import Task

        query = db.query(Task).filter(Task.user_id == user_id)

        # Apply filters if provided
        if filters:
            if 'status' in filters:
                query = query.filter(Task.status == filters['status'])

            if 'created_after' in filters:
                query = query.filter(Task.created_at >= filters['created_after'])

            if 'due_before' in filters:
                query = query.filter(Task.due_date <= filters['due_before'])

        # Order by created_at descending for better performance
        query = query.order_by(Task.created_at.desc())

        return query

    @staticmethod
    def batch_load_tasks(db, user_ids: list):
        """
        Batch load tasks for multiple users to reduce queries
        """
        from ..models.task import Task

        tasks = db.query(Task).filter(Task.user_id.in_(user_ids)).all()

        # Group tasks by user_id
        tasks_by_user = {}
        for task in tasks:
            if task.user_id not in tasks_by_user:
                tasks_by_user[task.user_id] = []
            tasks_by_user[task.user_id].append(task)

        return tasks_by_user


class ResponseOptimizer:
    """Optimize API responses"""

    @staticmethod
    def paginate_results(query, page: int = 1, page_size: int = 20):
        """
        Paginate query results for better performance
        """
        offset = (page - 1) * page_size
        total = query.count()
        items = query.offset(offset).limit(page_size).all()

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }

    @staticmethod
    def compress_response(data: dict):
        """
        Compress response data by removing null values
        """
        return {k: v for k, v in data.items() if v is not None}


# Connection pooling configuration
DATABASE_POOL_CONFIG = {
    'pool_size': 10,  # Number of connections to maintain
    'max_overflow': 20,  # Maximum number of connections to create beyond pool_size
    'pool_timeout': 30,  # Seconds to wait before giving up on getting a connection
    'pool_recycle': 3600,  # Recycle connections after 1 hour
    'pool_pre_ping': True  # Verify connections before using them
}
