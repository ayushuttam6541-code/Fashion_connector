import * as React from "react"
import { cn } from "../../lib/utils"

const Dialog = ({ open, onOpenChange, children }) => {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={() => onOpenChange(false)} />
      <div className="relative z-50 bg-white rounded-lg shadow-lg max-w-lg w-full mx-4">
        {children}
      </div>
    </div>
  )
}

const DialogContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <div ref={ref} className={cn("p-6", className)} {...props}>
    {children}
  </div>
))
DialogContent.displayName = "DialogContent"

const DialogHeader = ({ className, children, ...props }) => (
  <div className={cn("mb-4", className)} {...props}>
    {children}
  </div>
)
DialogHeader.displayName = "DialogHeader"

const DialogTitle = React.forwardRef(({ className, children, ...props }, ref) => (
  <h2 ref={ref} className={cn("text-lg font-semibold", className)} {...props}>
    {children}
  </h2>
))
DialogTitle.displayName = "DialogTitle"

const DialogTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <button ref={ref} className={className} {...props}>
    {children}
  </button>
))
DialogTrigger.displayName = "DialogTrigger"

export { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger }
