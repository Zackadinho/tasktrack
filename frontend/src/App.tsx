// The main screen. It owns the list of tasks and passes pieces down to smaller components.
import { useEffect, useState } from "react";
import { api } from "./api";
import type { Task } from "./types";
import TaskForm from "./components/TaskForm";
import TaskItem from "./components/TaskItem";

export default function App() {
  // "State" is data that, when it changes, makes React redraw the screen automatically.
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // useEffect with [] runs once, when the page first loads: fetch tasks from the backend.
  useEffect(() => {
    api
      .listTasks()
      .then(setTasks)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  // Each handler: call the backend first, then update local state with what it returned.
  async function handleCreate(title: string, description: string) {
    const created = await api.createTask(title, description);
    setTasks([created, ...tasks]);
  }

  async function handleToggle(task: Task) {
    try {
      const updated = await api.updateTask(task.id, { done: !task.done });
      setTasks(tasks.map((t) => (t.id === updated.id ? updated : t)));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function handleDelete(task: Task) {
    try {
      await api.deleteTask(task.id);
      setTasks(tasks.filter((t) => t.id !== task.id));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  const remaining = tasks.filter((t) => !t.done).length;

  return (
    <main className="container">
      <h1>TaskTrack</h1>
      <TaskForm onCreate={handleCreate} />

      {error && <p className="error">⚠ {error}</p>}
      {loading && <p className="muted">Loading…</p>}
      {!loading && tasks.length === 0 && !error && <p className="muted">No tasks yet. Add one above.</p>}

      <ul className="task-list">
        {tasks.map((task) => (
          <TaskItem key={task.id} task={task} onToggle={handleToggle} onDelete={handleDelete} />
        ))}
      </ul>

      {tasks.length > 0 && <p className="muted">{remaining} of {tasks.length} remaining</p>}
    </main>
  );
}
