import React from 'react'

const Tabs = ({ value, onValueChange, className, children, ...props }) => {
  return (
    <div className={className} {...props}>
      {React.Children.map(children, child => 
        React.cloneElement(child, { value, onValueChange })
      )}
    </div>
  )
}

const TabsList = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={`inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${className || ''}`}
    {...props}
  />
))
TabsList.displayName = "TabsList"

const TabsTrigger = React.forwardRef(({ className, value, onValueChange, children, ...props }, ref) => {
  const handleClick = () => {
    if (onValueChange) {
      onValueChange(value)
    }
  }

  return (
    <button
      ref={ref}
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm ${className || ''}`}
      onClick={handleClick}
      {...props}
    >
      {children}
    </button>
  )
})
TabsTrigger.displayName = "TabsTrigger"

const TabsContent = ({ className, value, children, ...props }) => {
  const currentValue = props.value || value
  const targetValue = props.targetValue || value
  
  if (currentValue !== targetValue) {
    return null
  }

  return (
    <div
      className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className || ''}`}
      {...props}
    >
      {children}
    </div>
  )
}
TabsContent.displayName = "TabsContent"

export { Tabs, TabsList, TabsTrigger, TabsContent }

