import { TodoItem } from "@/components/todo-item";
import type { Todo, TodoPriority } from "@/types/todo";

export interface TodoListProps {
  todos: Todo[];
  onToggleComplete?: (id: string, completed: boolean) => void;
  onTitleChange?: (id: string, title: string) => void;
  onPriorityChange?: (id: string, priority: TodoPriority) => void;
}

export function TodoList({
  todos,
  onToggleComplete,
  onTitleChange,
  onPriorityChange,
}: TodoListProps) {
  if (todos.length === 0) {
    return (
      <div className="px-4 py-8 text-center text-muted-foreground text-sm lg:px-6">
        No tasks yet. Add one to get started.
      </div>
    );
  }

  return (
    <div className="flex w-full max-h-[calc(100vh-13rem)] flex-col gap-3 overflow-y-auto px-4 lg:px-6">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggleComplete={onToggleComplete}
          onTitleChange={onTitleChange}
          onPriorityChange={onPriorityChange}
        />
      ))}
    </div>
  );
}
