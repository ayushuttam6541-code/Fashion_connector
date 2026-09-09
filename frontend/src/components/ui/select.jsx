import * as React from "react"
import { cn } from "../../lib/utils"

const Select = React.forwardRef(({ className, children, ...props }, ref) => (
  <div className="relative">
    <select
      className={cn(
        "flex h-10 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-700 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  </div>
))
Select.displayName = "Select"

const SelectTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <Select ref={ref} className={className} {...props}>
    {children}
  </Select>
))
SelectTrigger.displayName = "SelectTrigger"

const SelectValue = React.forwardRef(({ placeholder, ...props }, ref) => (
  <option value="" ref={ref} {...props}>
    {placeholder}
  </option>
))
SelectValue.displayName = "SelectValue"

const SelectContent = ({ children }) => <>{children}</>
const SelectItem = React.forwardRef(({ className, children, ...props }, ref) => (
  <option ref={ref} className={cn("className", className)} {...props}>
    {children}
  </option>
))
SelectItem.displayName = "SelectItem"

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem }
