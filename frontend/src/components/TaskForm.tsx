// A component is a reusable piece of UI: a function that returns what to draw.
// This one is the "add a task" form. It doesn't call the API itself; it tells its
// parent (App) via the onCreate "prop", the way a function receives arguments.
import { useState, type FormEvent } from "react";

interface Props {
  onCreate: (title: string, description: string) => Promise<void>;
}

export default function TaskForm({ onCreate }: Props) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault(); // stop the browser's default full-page reload
    setSaving(true);
    setError(null);
    try {
      await onCreate(title.trim(), description.trim());
      setTitle("");
      setDescription("");
    } catch (e) {
      setError((e as Error).message); // e.g. the backend's 422 message
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="What needs doing?"
        maxLength={200} // a convenience check for the user; the BACKEND is the real enforcer
        required
      />
      <input
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Details (optional)"
        maxLength={5000}
      />
      <button type="submit" disabled={saving || !title.trim()}>
        {saving ? "Adding…" : "Add task"}
      </button>
      {error && <p className="error">⚠ {error}</p>}
    </form>
  );
}
