import React from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

/**
 * Magic UI Animated Button Component
 * Features: Hover effects, click animations, gradient backgrounds
 */
export const MagicButton = React.forwardRef(({ 
  className, 
  variant = "default", 
  size = "default", 
  children, 
  disabled = false,
  loading = false,
  icon,
  ...props 
}, ref) => {
  const variants = {
    default: "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg hover:shadow-xl",
    secondary: "bg-gradient-to-r from-gray-100 to-gray-200 text-gray-900 shadow-md hover:shadow-lg dark:from-gray-800 dark:to-gray-700 dark:text-white",
    outline: "border-2 border-gradient-to-r from-blue-600 to-purple-600 bg-transparent text-blue-600 hover:bg-gradient-to-r hover:from-blue-600 hover:to-purple-600 hover:text-white",
    ghost: "bg-transparent hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 text-gray-700 dark:text-gray-300 dark:hover:from-gray-800 dark:hover:to-gray-700",
    destructive: "bg-gradient-to-r from-red-500 to-red-600 text-white shadow-lg hover:shadow-xl",
    magic: "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white shadow-2xl hover:shadow-purple-500/25 relative overflow-hidden"
  }

  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-8 px-3 text-sm",
    lg: "h-12 px-8 text-lg",
    icon: "h-10 w-10"
  }

  return (
    <motion.button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className
      )}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      disabled={disabled || loading}
      {...props}
    >
      {variant === "magic" && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
          initial={{ x: "-100%" }}
          animate={{ x: "100%" }}
          transition={{
            repeat: Infinity,
            duration: 2,
            ease: "linear"
          }}
        />
      )}
      
      {loading && (
        <motion.div
          className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      )}
      
      {icon && <span className="w-4 h-4">{icon}</span>}
      
      {children}
    </motion.button>
  )
})

MagicButton.displayName = "MagicButton"

/**
 * Magic UI Card Component with hover effects and gradients
 */
export const MagicCard = React.forwardRef(({ 
  className, 
  children, 
  variant = "default",
  gradient = false,
  glow = false,
  animated = false,
  ...props 
}, ref) => {
  const variants = {
    default: "bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800",
    primary: "bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0",
    secondary: "bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 border border-gray-200 dark:border-gray-600",
    error: "bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950 dark:to-red-900 border border-red-200 dark:border-red-800",
    gradient: "bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-gray-800 border border-gray-200/50 dark:border-gray-700/50",
    glass: "bg-white/10 backdrop-blur-md border border-white/20 dark:border-gray-800/50",
    magic: "bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 border border-indigo-200/50 dark:border-purple-800/50"
  }

  return (
    <motion.div
      ref={ref}
      className={cn(
        "rounded-xl shadow-sm transition-all duration-200 relative overflow-hidden",
        variants[variant],
        glow && "shadow-lg hover:shadow-xl",
        gradient && "shadow-gradient",
        className
      )}
      whileHover={{ 
        scale: 1.02,
        boxShadow: glow ? "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)" : undefined
      }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {animated && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/10 to-transparent"
          initial={{ x: "-100%" }}
          animate={{ x: "100%" }}
          transition={{
            repeat: Infinity,
            duration: 2,
            ease: "linear"
          }}
        />
      )}
      {children}
    </motion.div>
  )
})

MagicCard.displayName = "MagicCard"

/**
 * Magic UI Input Component with floating labels and animations
 */
export const MagicInput = React.forwardRef(({ 
  className, 
  type = "text", 
  placeholder,
  label,
  error,
  icon,
  ...props 
}, ref) => {
  const [focused, setFocused] = React.useState(false)
  const [hasValue, setHasValue] = React.useState(false)

  return (
    <div className="relative">
      <motion.div 
        className="relative"
        whileFocus={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 z-10">
            {icon}
          </div>
        )}
        
        <input
          ref={ref}
          type={type}
          className={cn(
            "w-full px-4 py-3 bg-white dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-lg",
            "transition-all duration-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10",
            "placeholder-transparent peer",
            icon && "pl-10",
            error && "border-red-500 focus:border-red-500 focus:ring-red-500/10",
            className
          )}
          placeholder={placeholder}
          onFocus={() => setFocused(true)}
          onBlur={(e) => {
            setFocused(false)
            setHasValue(e.target.value.length > 0)
          }}
          onChange={(e) => setHasValue(e.target.value.length > 0)}
          {...props}
        />
        
        {label && (
          <motion.label
            className={cn(
              "absolute left-4 transition-all duration-200 pointer-events-none",
              "text-gray-500 dark:text-gray-400",
              icon && "left-10",
              focused || hasValue 
                ? "-top-2 text-xs bg-white dark:bg-gray-900 px-2 text-blue-600 dark:text-blue-400" 
                : "top-1/2 transform -translate-y-1/2 text-sm"
            )}
            animate={{
              y: focused || hasValue ? -20 : 0,
              scale: focused || hasValue ? 0.85 : 1,
            }}
            transition={{ duration: 0.2 }}
          >
            {label}
          </motion.label>
        )}
      </motion.div>
      
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-1 text-sm text-red-500"
        >
          {error}
        </motion.p>
      )}
    </div>
  )
})

MagicInput.displayName = "MagicInput"

/**
 * Magic UI Textarea Component with auto-resize and animations
 */
export const MagicTextarea = React.forwardRef(({ 
  className, 
  placeholder,
  label,
  error,
  autoResize = true,
  maxHeight = 120,
  ...props 
}, ref) => {
  const [focused, setFocused] = React.useState(false)
  const [hasValue, setHasValue] = React.useState(false)

  const adjustHeight = React.useCallback(() => {
    if (autoResize && ref?.current) {
      ref.current.style.height = 'auto'
      ref.current.style.height = `${Math.min(ref.current.scrollHeight, maxHeight)}px`
    }
  }, [autoResize, maxHeight, ref])

  React.useEffect(() => {
    adjustHeight()
  }, [adjustHeight])

  return (
    <div className="relative">
      <motion.div 
        className="relative"
        whileFocus={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <textarea
          ref={ref}
          className={cn(
            "w-full px-4 py-3 bg-white dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-lg",
            "transition-all duration-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10",
            "placeholder-gray-500 dark:placeholder-gray-400 resize-none",
            autoResize && "overflow-hidden",
            error && "border-red-500 focus:border-red-500 focus:ring-red-500/10",
            className
          )}
          placeholder={placeholder}
          onFocus={() => setFocused(true)}
          onBlur={(e) => {
            setFocused(false)
            setHasValue(e.target.value.length > 0)
          }}
          onChange={(e) => {
            setHasValue(e.target.value.length > 0)
            adjustHeight()
            props.onChange?.(e)
          }}
          onInput={adjustHeight}
          style={{ minHeight: '40px' }}
          {...props}
        />
        
        {label && (
          <motion.label
            className={cn(
              "absolute left-4 transition-all duration-200 pointer-events-none",
              "text-gray-500 dark:text-gray-400",
              focused || hasValue 
                ? "-top-2 text-xs bg-white dark:bg-gray-900 px-2 text-blue-600 dark:text-blue-400" 
                : "top-3 text-sm"
            )}
            animate={{
              y: focused || hasValue ? -8 : 0,
              scale: focused || hasValue ? 0.85 : 1,
            }}
            transition={{ duration: 0.2 }}
          >
            {label}
          </motion.label>
        )}
      </motion.div>
      
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-1 text-sm text-red-500"
        >
          {error}
        </motion.p>
      )}
    </div>
  )
})

MagicTextarea.displayName = "MagicTextarea"

export default { MagicButton, MagicCard, MagicInput, MagicTextarea }
