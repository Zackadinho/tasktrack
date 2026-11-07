// This file is THE BRIDGE between frontend and backend.
// Every conversation with the API goes through here, and nothing else in the
// frontend knows URLs or HTTP details.
import type { Task } from "./types";

// Where the backend lives. It comes from an environment variable, like config.py on the backend.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

// One helper that sends a request, checks for errors, and parses the JSON reply.
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });

  if (!response.ok) {
    // e.g. 404 Task not found, 422 validation error
    const body = await response.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : `Request failed (${response.status})`;
    throw new Error(detail);
  }

  // 204 No Content (after DELETE) has no body to parse
  return (response.status === 204 ? undefined : await response.json()) as T;
}

// One function per backend endpoint. Compare these with backend/app/routers/tasks.py.
export const api = {
  listTasks: () => request<Task[]>("/tasks"),

  createTask: (title: string, description?: string) =>
    request<Task>("/tasks", {
      method: "POST",
      body: JSON.stringify({ title, description: description || null }),
    }),

  updateTask: (id: number, changes: Partial<Pick<Task, "title" | "description" | "done">>) =>
    request<Task>(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(changes) }),

  deleteTask: (id: number) => request<void>(`/tasks/${id}`, { method: "DELETE" }),
};
