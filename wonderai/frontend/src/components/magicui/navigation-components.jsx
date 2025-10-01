import React from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

/**
 * Magic UI Dialog/Modal Component with backdrop blur and animations
 */
export const MagicDialog = ({ 
  children, 
  open, 
  onClose, 
  className,
  size = "default",
  ...props 
}) => {
  const sizes = {
    sm: "max-w-md",
    default: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
    full: "max-w-7xl"
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <motion.div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        {...props}
      />
      
      {/* Dialog Content */}
      <motion.div
        className={cn(
          "relative w-full bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700",
          "bg-gradient-to-br from-white via-white to-gray-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800",
          sizes[size],
          className
        )}
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        transition={{ duration: 0.2 }}
      >
        {children}
      </motion.div>
    </div>
  )
}

/**
 * Magic UI Navigation with hover effects and active states
 */
export const MagicNav = React.forwardRef(({ 
  className, 
  children,
  orientation = "horizontal",
  ...props 
}, ref) => {
  return (
    <nav
      ref={ref}
      className={cn(
        "flex items-center space-x-1 p-1 rounded-lg bg-gray-100/50 dark:bg-gray-800/50 backdrop-blur-sm",
        orientation === "vertical" && "flex-col space-x-0 space-y-1",
        className
      )}
      {...props}
    >
      {children}
    </nav>
  )
})

MagicNav.displayName = "MagicNav"

/**
 * Magic UI Navigation Item with magnetic hover effects
 */
export const MagicNavItem = React.forwardRef(({ 
  className, 
  children,
  active = false,
  disabled = false,
  ...props 
}, ref) => {
  return (
    <motion.button
      ref={ref}
      className={cn(
        "relative px-3 py-2 rounded-md text-sm font-medium transition-all duration-200",
        "hover:bg-white/80 dark:hover:bg-gray-700/80 hover:shadow-sm",
        active && "bg-white dark:bg-gray-700 shadow-sm text-blue-600 dark:text-blue-400",
        disabled && "opacity-50 cursor-not-allowed",
        "text-gray-700 dark:text-gray-300",
        className
      )}
      whileHover={!disabled ? { scale: 1.05 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
      disabled={disabled}
      {...props}
    >
      {active && (
        <motion.div
          layoutId="navActiveIndicator"
          className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-md"
          initial={false}
          transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
        />
      )}
      <span className="relative z-10">{children}</span>
    </motion.button>
  )
})

MagicNavItem.displayName = "MagicNavItem"

/**
 * Magic UI Sidebar with slide animations
 */
export const MagicSidebar = React.forwardRef(({ 
  className, 
  children,
  open = true,
  side = "left",
  overlay = false,
  ...props 
}, ref) => {
  const sideClasses = {
    left: "left-0 border-r",
    right: "right-0 border-l",
    top: "top-0 border-b w-full",
    bottom: "bottom-0 border-t w-full"
  }

  const slideVariants = {
    left: { x: open ? 0 : "-100%" },
    right: { x: open ? 0 : "100%" },
    top: { y: open ? 0 : "-100%" },
    bottom: { y: open ? 0 : "100%" }
  }

  return (
    <>
      {overlay && open && (
        <motion.div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        />
      )}
      
      <motion.aside
        ref={ref}
        className={cn(
          "fixed z-50 h-full bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-gray-200 dark:border-gray-700",
          side === "left" || side === "right" ? "w-64" : "h-64",
          sideClasses[side],
          className
        )}
        animate={slideVariants[side]}
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        {...props}
      >
        <div className="h-full overflow-y-auto p-4">
          {children}
        </div>
      </motion.aside>
    </>
  )
})

MagicSidebar.displayName = "MagicSidebar"

/**
 * Magic UI Tabs with smooth indicator animation
 */
export const MagicTabs = ({ 
  value, 
  onValueChange, 
  children, 
  className,
  orientation = "horizontal",
  ...props 
}) => {
  return (
    <div 
      className={cn(
        "w-full",
        orientation === "vertical" && "flex gap-4",
        className
      )}
      {...props}
    >
      {React.Children.map(children, child => 
        React.cloneElement(child, { value, onValueChange, orientation })
      )}
    </div>
  )
}

export const MagicTabsList = ({ 
  children, 
  value, 
  onValueChange, 
  orientation = "horizontal",
  className,
  ...props 
}) => {
  return (
    <div
      className={cn(
        "relative inline-flex p-1 rounded-lg bg-gray-100 dark:bg-gray-800",
        orientation === "vertical" && "flex-col",
        className
      )}
      {...props}
    >
      {React.Children.map(children, child => 
        React.cloneElement(child, { value, onValueChange, orientation })
      )}
    </div>
  )
}

export const MagicTabsTrigger = ({ 
  children, 
  tabValue, 
  value, 
  onValueChange,
  orientation = "horizontal",
  className,
  ...props 
}) => {
  const isActive = value === tabValue

  return (
    <motion.button
      className={cn(
        "relative px-3 py-2 text-sm font-medium rounded-md transition-colors",
        "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100",
        isActive && "text-gray-900 dark:text-white",
        className
      )}
      onClick={() => onValueChange?.(tabValue)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      {...props}
    >
      {isActive && (
        <motion.div
          layoutId="tabIndicator"
          className="absolute inset-0 bg-white dark:bg-gray-700 rounded-md shadow-sm"
          initial={false}
          transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
        />
      )}
      <span className="relative z-10">{children}</span>
    </motion.button>
  )
}

export const MagicTabsContent = ({ 
  children, 
  tabValue, 
  value,
  className,
  ...props 
}) => {
  if (value !== tabValue) return null

  return (
    <motion.div
      className={cn("mt-4", className)}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {children}
    </motion.div>
  )
}

export default { 
  MagicDialog, 
  MagicNav, 
  MagicNavItem, 
  MagicSidebar, 
  MagicTabs, 
  MagicTabsList, 
  MagicTabsTrigger, 
  MagicTabsContent 
}
