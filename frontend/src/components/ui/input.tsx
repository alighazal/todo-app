import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef<
  HTMLInputElement,
  React.ComponentProps<"input">
>(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      data-slot="input"
      ref={ref}
      className={cn(
        "w-full rounded-md border border-input p-2 text-sm text-foreground shadow-none",
        "placeholder:text-muted-foreground hover:bg-muted/50",
        "focus-visible:border-primary focus-visible:outline focus-visible:outline-0 focus-visible:outline-primary focus-visible:outline-offset-0",
        className
      )}
      {...props}
    />
  )
})
Input.displayName = "Input"

export { Input }
