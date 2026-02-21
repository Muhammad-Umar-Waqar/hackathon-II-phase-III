import React, { useState } from 'react';
import { taskAPI } from '../services/api';

const TaskItem = ({ task, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: task.title,
    description: task.description || '',
    status: task.status,
    due_date: task.due_date ? new Date(task.due_date).toISOString().split('T')[0] : ''
  });

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
    setEditData({
      title: task.title,
      description: task.description || '',
      status: task.status,
      due_date: task.due_date ? new Date(task.due_date).toISOString().split('T')[0] : ''
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();

    try {
      const updatePayload = {
        ...editData
      };

      // Convert date back to proper format if provided
      if (updatePayload.due_date) {
        updatePayload.due_date = new Date(updatePayload.due_date).toISOString();
      }

      await taskAPI.update(task.id, updatePayload);
      onUpdate(task.id, { ...task, ...editData });
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.delete(task.id);
        onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const handleStatusChange = async (newStatus) => {
    try {
      await taskAPI.update(task.id, { status: newStatus });
      onUpdate(task.id, { ...task, status: newStatus });
    } catch (error) {
      console.error('Error updating task status:', error);
      alert('Failed to update task status. Please try again.');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in-progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'pending':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="border rounded-lg p-4 mb-3 shadow-sm hover:shadow-md transition-shadow w-full">
      {isEditing ? (
        <form onSubmit={handleSave} className="space-y-3 w-full">
          <input
            type="text"
            name="title"
            value={editData.title}
            onChange={handleInputChange}
            className="w-full p-2 border rounded mb-2 responsive-input"
            required
          />

          <textarea
            name="description"
            value={editData.description}
            onChange={handleInputChange}
            className="w-full p-2 border rounded mb-2 responsive-input"
            rows="2"
            placeholder="Description (optional)"
          />

          <div className="flex flex-col sm:flex-row gap-2 w-full">
            <select
              name="status"
              value={editData.status}
              onChange={handleInputChange}
              className="p-2 border rounded responsive-input flex-grow"
            >
              <option value="pending">Pending</option>
              <option value="in-progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>

            <input
              type="date"
              name="due_date"
              value={editData.due_date}
              onChange={handleInputChange}
              className="p-2 border rounded responsive-input flex-grow"
            />
          </div>

          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2 mt-3">
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 responsive-button"
            >
              Save
            </button>
            <button
              type="button"
              onClick={handleEditToggle}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 responsive-button"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="space-y-2 w-full">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2">
            <h3 className="font-semibold text-lg break-words">{task.title}</h3>
            <div className="flex space-x-2 self-start sm:self-auto">
              <button
                onClick={handleEditToggle}
                className="text-blue-500 hover:text-blue-700 text-sm responsive-button"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="text-red-500 hover:text-red-700 text-sm responsive-button"
              >
                Delete
              </button>
            </div>
          </div>

          {task.description && (
            <p className="text-gray-600 text-sm break-words">{task.description}</p>
          )}

          <div className="flex flex-wrap items-center gap-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusClass(task.status)} break-words`}>
              {task.status.replace('-', ' ')}
            </span>

            {task.due_date && (
              <span className="text-xs text-gray-500 break-words">
                Due: {formatDate(task.due_date)}
              </span>
            )}

            <span className="text-xs text-gray-500 break-words">
              Created: {formatDate(task.created_at)}
            </span>
          </div>

          <div className="mt-2 flex flex-wrap gap-1">
            {['pending', 'in-progress', 'completed'].map((status) => (
              <button
                key={status}
                onClick={() => handleStatusChange(status)}
                disabled={task.status === status}
                className={`text-xs px-2 py-1 rounded ${
                  task.status === status
                    ? 'bg-gray-300 text-gray-700 cursor-default'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                } responsive-button`}
              >
                {status.replace('-', ' ')}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;