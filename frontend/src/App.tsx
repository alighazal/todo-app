import { useState } from "react";
import { AppSidebar } from "@/components/app-sidebar";
import { TodoList } from "@/components/todo-list";
import { SiteHeader } from "@/components/site-header";
import { Button } from "@/components/ui/button";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import type { Todo, TodoPriority } from "@/types/todo";

const initialTodos: Todo[] = [
  {
    id: "1",
    title: "Review project proposal",
    details: "Go through the draft and add feedback for the design section.",
    priority: "high",
    createdAt: "2025-03-10T09:00:00Z",
    deadline: "2025-03-15T17:00:00Z",
    completed: false,
  },
  {
    id: "2",
    title: "Update documentation",
    details: "Sync README and API docs with the latest changes.",
    priority: "medium",
    createdAt: "2025-03-12T14:30:00Z",
    completed: false,
  },
  {
    id: "3",
    title: "Fix login redirect bug",
    priority: "low",
    createdAt: "2025-03-13T11:00:00Z",
    completed: true,
  },
  {
    id: "4",
    title: "Fix login redirect bug",
    priority: "low",
    createdAt: "2025-03-13T11:00:00Z",
    completed: true,
  },
];

function App() {
  const [todos, setTodos] = useState<Todo[]>(initialTodos);

  const handleToggleComplete = (id: string, completed: boolean) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, completed } : t))
    );
  };

  const handleTitleChange = (id: string, title: string) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, title } : t))
    );
  };

  const handlePriorityChange = (id: string, priority: TodoPriority) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, priority } : t))
    );
  };

  const handleAddTask = () => {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      title: "",
      createdAt: new Date().toISOString(),
      completed: false,
      priority: "low",
    };
    setTodos((prev) => [newTodo, ...prev]);
  };

  return (
    <>
      <div>
        <SidebarProvider
          style={
            {
              "--sidebar-width": "calc(var(--spacing) * 72)",
              "--header-height": "calc(var(--spacing) * 12)",
            } as React.CSSProperties
          }
        >
          <AppSidebar variant="inset" />
          <SidebarInset>
            <SiteHeader />
            <div className="flex flex-1 flex-col">
              <div className="@container/main flex flex-1 flex-col gap-2">
                <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
                  <div className="flex justify-end px-4 lg:px-6">
                    <Button onClick={handleAddTask}>Add Task</Button>
                  </div>
                  <TodoList todos={todos} onToggleComplete={handleToggleComplete} onTitleChange={handleTitleChange} onPriorityChange={handlePriorityChange} />
                </div>
              </div>
            </div>
          </SidebarInset>
        </SidebarProvider>
      </div>
    </>
  );
}

export default App;
