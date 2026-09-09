import * as React from "react"
import { cn } from "../../lib/utils"

const TabsContext = React.createContext({})

const Tabs = ({ defaultValue, value, onValueChange, children, className }) => {
  const [activeTab, setActiveTab] = React.useState(value || defaultValue)

  const handleValueChange = (newValue) => {
    setActiveTab(newValue)
    if (onValueChange) onValueChange(newValue)
  }

  return (
    <TabsContext.Provider value={{ activeTab, handleValueChange }}>
      <div className={cn("", className)}>{children}</div>
    </TabsContext.Provider>
  )
}

const TabsList = ({ className, children }) => {
  const { activeTab, handleValueChange } = React.useContext(TabsContext)
  
  return (
    <div className={cn("inline-flex h-10 items-center justify-center rounded-md bg-slate-100 p-1", className)}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            isActive: child.props.value === activeTab,
            onClick: () => handleValueChange(child.props.value)
          })
        }
        return child
      })}
    </div>
  )
}

const TabsTrigger = React.forwardRef(({ className, value, isActive, onClick, children, ...props }, ref) => (
  <button
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-white transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-700 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
      isActive ? "bg-white text-slate-900 shadow-sm" : "text-slate-500 hover:text-slate-900",
      className
    )}
    onClick={onClick}
    {...props}
  >
    {children}
  </button>
))
TabsTrigger.displayName = "TabsTrigger"

const TabsContent = ({ value, className, children, ...props }) => {
  const { activeTab } = React.useContext(TabsContext)
  
  if (value !== activeTab) return null
  
  return (
    <div className={cn("mt-2 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-700 focus-visible:ring-offset-2", className)} {...props}>
      {children}
    </div>
  )
}
TabsContent.displayName = "TabsContent"

export { Tabs, TabsList, TabsTrigger, TabsContent }
