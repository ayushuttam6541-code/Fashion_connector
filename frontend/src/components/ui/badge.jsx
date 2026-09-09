import * as React from "react"
import { cn } from "../../lib/utils"

const Badge = React.forwardRef(({ className, variant = "default", ...props }, ref) => {
  const variants = {
    default: "bg-orange-100 text-orange-700 border-orange-200",
    secondary: "bg-slate-100 text-slate-700 border-slate-200",
    destructive: "bg-red-100 text-red-700 border-red-200",
    outline: "text-slate-700 border-slate-200",
    success: "bg-emerald-100 text-emerald-700 border-emerald-200",
  }

  return (
    <div
      ref={ref}
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-orange-700 focus:ring-offset-2",
        variants[variant],
        className
      )}
      {...props}
    />
  )
})
Badge.displayName = "Badge"

export { Badge }
