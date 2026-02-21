import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskForm from '../../src/components/TaskForm';

describe('TaskForm Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders empty form for new task', () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    expect(screen.getByLabelText(/title/i)).toHaveValue('');
    expect(screen.getByLabelText(/description/i)).toHaveValue('');
    expect(screen.getByLabelText(/status/i)).toHaveValue('pending');
  });

  test('renders form with existing task data', () => {
    const existingTask = {
      id: 1,
      title: 'Existing Task',
      description: 'Existing Description',
      status: 'in-progress',
      user_id: 1
    };

    render(
      <TaskForm
        task={existingTask}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText(/title/i)).toHaveValue('Existing Task');
    expect(screen.getByLabelText(/description/i)).toHaveValue('Existing Description');
    expect(screen.getByLabelText(/status/i)).toHaveValue('in-progress');
  });

  test('validates required title field', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('validates title length', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    const longTitle = 'a'.repeat(201); // Exceeds 200 character limit

    fireEvent.change(titleInput, { target: { value: longTitle } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title must be 200 characters or less/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('validates description length', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const longDescription = 'a'.repeat(1001); // Exceeds 1000 character limit

    fireEvent.change(titleInput, { target: { value: 'Valid Title' } });
    fireEvent.change(descriptionInput, { target: { value: longDescription } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/description must be 1000 characters or less/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('submits form with valid data', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const statusSelect = screen.getByLabelText(/status/i);

    fireEvent.change(titleInput, { target: { value: 'New Task' } });
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });
    fireEvent.change(statusSelect, { target: { value: 'in-progress' } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'New Description',
        status: 'in-progress'
      });
    });
  });

  test('calls onCancel when cancel button is clicked', () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('displays all status options', () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const statusSelect = screen.getByLabelText(/status/i);
    const options = statusSelect.querySelectorAll('option');

    expect(options).toHaveLength(3);
    expect(options[0]).toHaveValue('pending');
    expect(options[1]).toHaveValue('in-progress');
    expect(options[2]).toHaveValue('completed');
  });

  test('clears form after successful submission', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: 'New Task' } });
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalled();
    });

    // Form should be cleared after submission
    expect(titleInput).toHaveValue('');
    expect(descriptionInput).toHaveValue('');
  });

  test('is accessible with proper labels and ARIA attributes', () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const statusSelect = screen.getByLabelText(/status/i);

    expect(titleInput).toHaveAttribute('id');
    expect(descriptionInput).toHaveAttribute('id');
    expect(statusSelect).toHaveAttribute('id');

    expect(titleInput).toHaveAttribute('aria-required', 'true');
  });

  test('handles loading state during submission', async () => {
    const slowSubmit = jest.fn(() => new Promise(resolve => setTimeout(resolve, 1000)));

    render(<TaskForm onSubmit={slowSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    // Button should be disabled during submission
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/submitting|saving/i)).toBeInTheDocument();
  });

  test('displays error message on submission failure', async () => {
    const failingSubmit = jest.fn(() => Promise.reject(new Error('Submission failed')));

    render(<TaskForm onSubmit={failingSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const submitButton = screen.getByRole('button', { name: /submit|save/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/failed to save task/i)).toBeInTheDocument();
    });
  });
});
