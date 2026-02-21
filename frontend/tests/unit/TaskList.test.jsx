import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskList from '../../src/components/TaskList';

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: 1,
      title: 'Task 1',
      description: 'Description 1',
      status: 'pending',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      user_id: 1
    },
    {
      id: 2,
      title: 'Task 2',
      description: 'Description 2',
      status: 'in-progress',
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
      user_id: 1
    },
    {
      id: 3,
      title: 'Task 3',
      description: 'Description 3',
      status: 'completed',
      created_at: '2024-01-03T00:00:00Z',
      updated_at: '2024-01-03T00:00:00Z',
      user_id: 1
    }
  ];

  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders all tasks in the list', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
    expect(screen.getByText('Task 3')).toBeInTheDocument();
  });

  test('renders empty state when no tasks', () => {
    render(
      <TaskList
        tasks={[]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText(/no tasks/i)).toBeInTheDocument();
  });

  test('filters tasks by status', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    // Click on "In Progress" filter
    const inProgressFilter = screen.getByRole('button', { name: /in progress/i });
    fireEvent.click(inProgressFilter);

    // Should only show in-progress tasks
    expect(screen.getByText('Task 2')).toBeInTheDocument();
    expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
    expect(screen.queryByText('Task 3')).not.toBeInTheDocument();
  });

  test('shows all tasks when "All" filter is selected', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const allFilter = screen.getByRole('button', { name: /all/i });
    fireEvent.click(allFilter);

    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
    expect(screen.getByText('Task 3')).toBeInTheDocument();
  });

  test('passes update callback to task items', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const editButtons = screen.getAllByRole('button', { name: /edit/i });
    fireEvent.click(editButtons[0]);

    expect(mockOnUpdate).toHaveBeenCalledWith(mockTasks[0]);
  });

  test('passes delete callback to task items', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const deleteButtons = screen.getAllByRole('button', { name: /delete/i });
    fireEvent.click(deleteButtons[0]);

    await waitFor(() => {
      expect(mockOnDelete).toHaveBeenCalledWith(mockTasks[0].id);
    });
  });

  test('displays task count', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText(/3 tasks/i)).toBeInTheDocument();
  });

  test('is responsive and accessible', () => {
    const { container } = render(
      <TaskList
        tasks={mockTasks}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    );

    const list = container.querySelector('[role="list"]');
    expect(list).toBeInTheDocument();
    expect(list).toHaveAttribute('aria-label');
  });

  test('handles loading state', () => {
    render(
      <TaskList
        tasks={[]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        loading={true}
      />
    );

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('handles error state', () => {
    render(
      <TaskList
        tasks={[]}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        error="Failed to load tasks"
      />
    );

    expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument();
  });
});
