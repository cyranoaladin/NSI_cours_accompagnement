import React from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { cn } from '../../lib/utils';

const Select = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <select
      className={cn(
        "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  );
});

Select.displayName = "Select";

const SelectContent = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "relative z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});

SelectContent.displayName = "SelectContent";

const SelectItem = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <option
      ref={ref}
      className={cn(
        "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
        className
      )}
      {...props}
    >
      {children}
    </option>
  );
});

SelectItem.displayName = "SelectItem";

const SelectTrigger = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <button
      ref={ref}
      className={cn(
        "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 opacity-50" />
    </button>
  );
});

SelectTrigger.displayName = "SelectTrigger";

const SelectValue = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <span
      ref={ref}
      className={cn("block truncate", className)}
      {...props}
    />
  );
});

SelectValue.displayName = "SelectValue";

export {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
};

