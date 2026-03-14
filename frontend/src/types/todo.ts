export type TodoPriority = "low" | "medium" | "high";

export interface Todo {
  id: string;
  title: string;
  details?: string;
  priority?: TodoPriority;
  createdAt: string;
  deadline?: string;
  completed: boolean;
}
