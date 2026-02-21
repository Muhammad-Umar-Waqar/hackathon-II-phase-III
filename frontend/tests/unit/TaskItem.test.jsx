import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskItem from '../../src/components/TaskItem';

describe('TaskItem Component', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    status: 'pending',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    user_id: 1
  };

  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders task item with correct information', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText(/pending/i)).toBeInTheDocument();
  });

  test('calls onUpdate when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);

    expect(mockOnUpdate).toHaveBeenCalledWith(mockTask);
  });

  test('calls onDelete when delete button is clicked', async () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id);
    });
  });

  test('displays correct status badge color', () => {
    const { rerender } = render(
      <TaskItem
        task={{ ...mockTask, status: 'pending' }}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    let statusBadge = screen.getByText(/pending/i);
    expect(statusBadge).toHaveClass('status-pending');

    rerender(
      <TaskItem
        task={{ ...mockTask, status: 'in-progress' }}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    statusBadge = screen.getByText(/in-progress/i);
    expect(statusBadge).toHaveClass('status-in-progress');

    rerender(
      <TaskItem
        task={{ ...mockTask, status: 'completed' }}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    statusBadge = screen.getByText(/completed/i);
    expect(statusBadge).toHaveClass('status-completed');
  });

  test('handles missing description gracefully', () => {
    const taskWithoutDescription = { ...mockTask, description: null };

    render(
      <TaskItem
        task={taskWithoutDescription}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.queryByText('Test Description')).not.toBeInTheDocument();
  });

  test('is accessible with proper ARIA labels', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const editButton = screen.getByRole('button', { name: /edit/i });
    const deleteButton = screen.getByRole('button', { name: /delete/i });

    expect(editButton).toHaveAttribute('aria-label');
    expect(deleteButton).toHaveAttribute('aria-label');
  });
});
