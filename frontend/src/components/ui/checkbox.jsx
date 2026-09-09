import * as React from "react"
import { cn } from "../../lib/utils"

const Checkbox = React.forwardRef(({ className, checked, onChange, ...props }, ref) => {
  return (
    <input
      type="checkbox"
      ref={ref}
      checked={checked}
      onChange={onChange}
      className={cn(
        "h-4 w-4 rounded border-slate-300 text-orange-700 focus:ring-orange-700",
        className
      )}
      {...props}
    />
  )
})
Checkbox.displayName = "Checkbox"

export { Checkbox }
