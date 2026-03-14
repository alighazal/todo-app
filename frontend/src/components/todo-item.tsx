import * as React from "react";

import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import type { Todo, TodoPriority } from "@/types/todo";

const PRIORITIES: TodoPriority[] = ["low", "medium", "high"];

export interface TodoItemProps {
  todo: Todo;
  onToggleComplete?: (id: string, completed: boolean) => void;
  onTitleChange?: (id: string, title: string) => void;
  onPriorityChange?: (id: string, priority: TodoPriority) => void;
}

export function TodoItem({
  todo,
  onToggleComplete,
  onTitleChange,
  onPriorityChange,
}: TodoItemProps) {
  const [isEditing, setIsEditing] = React.useState(false);
  const [editValue, setEditValue] = React.useState(todo.title);
  const inputRef = React.useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    if (isEditing) {
      setEditValue(todo.title);
      inputRef.current?.focus();
    }
  }, [isEditing, todo.title]);

  const handleCheckboxChange = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  const handleCheckedChange = (checked: boolean | "indeterminate") => {
    onToggleComplete?.(todo.id, checked === true);
  };

  const handleTitleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsEditing(true);
  };

  const saveTitle = () => {
    const trimmed = editValue.trim();
    onTitleChange?.(todo.id, trimmed);
    setIsEditing(false);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      saveTitle();
    }
    if (e.key === "Escape") {
      setEditValue(todo.title);
      setIsEditing(false);
      inputRef.current?.blur();
    }
  };

  return (
    <Card className="flex flex-row items-center gap-3 px-4 py-3">
      <div onClick={handleCheckboxChange}>
        <Checkbox
          checked={todo.completed}
          onCheckedChange={handleCheckedChange}
          aria-label={`Mark "${todo.title || "task"}" as ${todo.completed ? "incomplete" : "complete"}`}
        />
      </div>
      <div className="min-w-0 flex-1">
        {isEditing ? (
          <Input
            ref={inputRef}
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={saveTitle}
            onKeyDown={handleInputKeyDown}
            placeholder="Task title goes here"
            className={cn(
              "min-h-8 rounded border-0 bg-transparent px-1 py-1 font-medium shadow-none focus-visible:ring-0 -mx-1 text-inherit text-[length:inherit] placeholder:italic placeholder:text-muted-foreground",
              todo.completed && "text-muted-foreground line-through"
            )}
            onClick={(e) => e.stopPropagation()}
          />
        ) : (
          <span
            role="button"
            tabIndex={0}
            onClick={handleTitleClick}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                e.stopPropagation();
                handleTitleClick(e as unknown as React.MouseEvent);
              }
            }}
            className={cn(
              "block min-h-8 rounded px-1 font-medium cursor-text hover:bg-muted/50 -mx-1 py-1",
              todo.completed && "text-muted-foreground line-through",
              !todo.title && "text-muted-foreground italic"
            )}
          >
            {todo.title || "Task title goes here"}
          </span>
        )}
      </div>
      <Select
        value={todo.priority ?? ""}
        onValueChange={(value: string) =>
          value && onPriorityChange?.(todo.id, value as TodoPriority)
        }
      >
        <SelectTrigger
          size="sm"
          className="shrink-0 w-[7rem] capitalize"
        >
          <SelectValue placeholder="Priority" />
        </SelectTrigger>
        <SelectContent>
          {PRIORITIES.map((p) => (
            <SelectItem key={p} value={p} className="capitalize">
              {p}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </Card>
  );
}
