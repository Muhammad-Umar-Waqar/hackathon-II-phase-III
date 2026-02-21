// Accessibility improvements for responsive design
import React from 'react';

// Accessible TaskItem component
export const AccessibleTaskItem = ({ task, onUpdate, onDelete }) => {
  return (
    <div
      className="task-item bg-white border border-gray-200 rounded-lg p-4 mb-3 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500"
      role="region"
      aria-labelledby={`task-title-${task.id}`}
      tabIndex="-1"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <h3
            id={`task-title-${task.id}`}
            className="text-lg font-medium text-gray-900 truncate"
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="mt-1 text-sm text-gray-600 line-clamp-2" aria-label={`Task description: ${task.description}`}>
              {task.description}
            </p>
          )}

          <div className="mt-2 flex flex-wrap gap-2">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                task.status === 'completed' ? 'bg-green-100 text-green-800' :
                task.status === 'in-progress' ? 'bg-yellow-100 text-yellow-800' :
                'bg-blue-100 text-blue-800'
              }`}
              aria-label={`Status: ${task.status.replace('-', ' ')}`}
            >
              {task.status.replace('-', ' ')}
            </span>

            {task.due_date && (
              <span
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                aria-label={`Due date: ${new Date(task.due_date).toLocaleDateString()}`}
              >
                Due: {new Date(task.due_date).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        <div className="ml-4 flex flex-shrink-0 space-x-2">
          <button
            onClick={() => onUpdate(task)}
            className="relative inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 min-h-9 min-w-9"
            aria-label={`Edit task: ${task.title}`}
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          <button
            onClick={() => onDelete(task)}
            className="relative inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 min-h-9 min-w-9"
            aria-label={`Delete task: ${task.title}`}
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

// Accessible TaskForm component
export const AccessibleTaskForm = ({ onSubmit, onCancel, task = null }) => {
  const [formData, setFormData] = React.useState({
    title: task?.title || '',
    description: task?.description || '',
    status: task?.status || 'pending',
    due_date: task?.due_date || ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ ...formData, id: task?.id });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
          minLength={1}
          maxLength={200}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border min-h-10"
          aria-describedby="title-help title-error"
          placeholder="Enter task title"
        />
        <p id="title-help" className="mt-1 text-sm text-gray-500">
          Enter a title for your task (required, max 200 characters)
        </p>
        <div id="title-error" role="alert" className="sr-only"></div>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          maxLength={1000}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          aria-describedby="description-help"
          placeholder="Enter task description (optional)"
        ></textarea>
        <p id="description-help" className="mt-1 text-sm text-gray-500">
          Describe your task in detail (optional, max 1000 characters)
        </p>
      </div>

      <div>
        <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          id="status"
          name="status"
          value={formData.status}
          onChange={handleChange}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          aria-describedby="status-help"
        >
          <option value="pending">Pending</option>
          <option value="in-progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <p id="status-help" className="mt-1 text-sm text-gray-500">
          Select the current status of your task
        </p>
      </div>

      <div>
        <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
          Due Date
        </label>
        <input
          type="date"
          id="due_date"
          name="due_date"
          value={formData.due_date}
          onChange={handleChange}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border min-h-10"
          aria-describedby="due-date-help"
        />
        <p id="due-date-help" className="mt-1 text-sm text-gray-500">
          Optional due date for your task
        </p>
      </div>

      <div className="flex space-x-3 pt-2">
        <button
          type="submit"
          disabled={!formData.title.trim()}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label={task ? "Update task" : "Create task"}
        >
          {task ? 'Update Task' : 'Create Task'}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            aria-label="Cancel form"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

// Accessible TaskList component
export const AccessibleTaskList = ({ tasks, onEdit, onDelete }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <div
        className="text-center py-12"
        role="status"
        aria-live="polite"
      >
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div
      className="space-y-3"
      role="list"
      aria-label="List of tasks"
    >
      {tasks.map((task) => (
        <AccessibleTaskItem
          key={task.id}
          task={task}
          onUpdate={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

// Accessibility utilities
export const AccessibilityUtils = {
  // Focus management helper
  focusFirstElement: (containerRef) => {
    if (containerRef.current) {
      const firstFocusableElement = containerRef.current.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (firstFocusableElement) {
        firstFocusableElement.focus();
      }
    }
  },

  // Announce to screen readers
  announce: (message) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  },

  // Keyboard navigation handler
  handleKeyDown: (event, handlers) => {
    switch (event.key) {
      case 'Enter':
      case ' ':
        if (handlers.onEnter) {
          event.preventDefault();
          handlers.onEnter();
        }
        break;
      case 'Escape':
        if (handlers.onEscape) {
          event.preventDefault();
          handlers.onEscape();
        }
        break;
      case 'ArrowDown':
        if (handlers.onArrowDown) {
          event.preventDefault();
          handlers.onArrowDown();
        }
        break;
      case 'ArrowUp':
        if (handlers.onArrowUp) {
          event.preventDefault();
          handlers.onArrowUp();
        }
        break;
    }
  }
};