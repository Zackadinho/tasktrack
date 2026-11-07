// One row in the task list: a checkbox, the text, and a delete button.
import type { Task } from "../types";

interface Props {
  task: Task;
  onToggle: (task: Task) => void;
  onDelete: (task: Task) => void;
}

export default function TaskItem({ task, onToggle, onDelete }: Props) {
  return (
    <li className={task.done ? "task done" : "task"}>
      <input type="checkbox" checked={task.done} onChange={() => onToggle(task)} aria-label="Mark done" />
      <div className="task-text">
        {/* React escapes this text automatically, so a title like <script>…</script>
            shows up as plain text instead of running. That blocks XSS attacks. */}
        <span className="task-title">{task.title}</span>
        {task.description && <span className="task-desc">{task.description}</span>}
      </div>
      <button className="delete" onClick={() => onDelete(task)} aria-label="Delete task">
        ✕
      </button>
    </li>
  );
}
