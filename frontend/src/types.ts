// The shape of a task, matching TaskOut in backend/app/schemas.py.
// If the backend and this file disagree, TypeScript complains while you code,
// not your users in production.
export interface Task {
  id: number;
  title: string;
  description: string | null;
  done: boolean;
  created_at: string; // JSON has no date type, so dates arrive as text
}
