import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import TaskItem from './TaskItem';
import { taskAPI } from '../services/api';

const TaskList = forwardRef(({ userId, onTaskUpdate, onTaskDelete }, ref) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskAPI.getAll();
      setTasks(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Expose refreshTasks method to parent component
  useImperativeHandle(ref, () => ({
    refreshTasks: fetchTasks
  }));

  const handleTaskUpdate = (taskId, updatedTask) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId ? updatedTask : task
      )
    );
    if (onTaskUpdate) onTaskUpdate(updatedTask);
  };

  const handleTaskDelete = (taskId) => {
    setTasks(prevTasks =>
      prevTasks.filter(task => task.id !== taskId)
    );
    if (onTaskDelete) onTaskDelete(taskId);
  };

  const filterTasksByStatus = (status) => {
    return tasks.filter(task => task.status === status);
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        <p className="mt-2 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error! </strong>
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">Pending</h3>
          <p className="text-2xl font-bold text-blue-600">
            {filterTasksByStatus('pending').length}
          </p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-yellow-800">In Progress</h3>
          <p className="text-2xl font-bold text-yellow-600">
            {filterTasksByStatus('in-progress').length}
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800">Completed</h3>
          <p className="text-2xl font-bold text-green-600">
            {filterTasksByStatus('completed').length}
          </p>
        </div>
      </div>

      {/* Task Lists by Status */}
      <div className="space-y-8">
        <div>
          <h3 className="text-xl font-semibold mb-3 text-gray-800">Pending Tasks</h3>
          {filterTasksByStatus('pending').length === 0 ? (
            <p className="text-gray-500 italic">No pending tasks</p>
          ) : (
            filterTasksByStatus('pending').map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
              />
            ))
          )}
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3 text-gray-800">In Progress</h3>
          {filterTasksByStatus('in-progress').length === 0 ? (
            <p className="text-gray-500 italic">No tasks in progress</p>
          ) : (
            filterTasksByStatus('in-progress').map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
              />
            ))
          )}
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3 text-gray-800">Completed Tasks</h3>
          {filterTasksByStatus('completed').length === 0 ? (
            <p className="text-gray-500 italic">No completed tasks</p>
          ) : (
            filterTasksByStatus('completed').map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
              />
            ))
          )}
        </div>
      </div>

      {/* Refresh Button */}
      <div className="mt-6">
        <button
          onClick={fetchTasks}
          className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Refresh Tasks
        </button>
      </div>
    </div>
  );
});

TaskList.displayName = 'TaskList';

export default TaskList;