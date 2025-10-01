import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { cn } from '@/lib/utils'

/**
 * Magic UI Avatar Component with animated borders and status indicators
 */
export const MagicAvatar = React.forwardRef(({ 
  className, 
  src, 
  alt, 
  fallback,
  size = "default",
  status,
  online = false,
  ...props 
}, ref) => {
  const sizes = {
    sm: "w-8 h-8",
    default: "w-10 h-10",
    lg: "w-12 h-12",
    xl: "w-16 h-16"
  }

  return (
    <motion.div 
      ref={ref}
      className={cn("relative inline-flex", className)}
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      <div className={cn(
        "relative overflow-hidden rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 p-0.5",
        sizes[size]
      )}>
        <div className="w-full h-full rounded-full bg-white dark:bg-gray-900 p-0.5">
          {src ? (
            <img
              src={src}
              alt={alt}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            <div className="w-full h-full rounded-full bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-600 flex items-center justify-center text-gray-600 dark:text-gray-300 font-medium">
              {fallback}
            </div>
          )}
        </div>
      </div>
      
      {(status || online) && (
        <motion.div
          className={cn(
            "absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white dark:border-gray-900",
            online ? "bg-green-500" : status === "busy" ? "bg-red-500" : status === "away" ? "bg-yellow-500" : "bg-gray-400"
          )}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
        />
      )}
    </motion.div>
  )
})

MagicAvatar.displayName = "MagicAvatar"

/**
 * Magic UI Badge Component with glow effects and animations
 */
export const MagicBadge = React.forwardRef(({ 
  className, 
  variant = "default",
  children,
  pulse = false,
  glow = false,
  ...props 
}, ref) => {
  const variants = {
    default: "bg-gradient-to-r from-blue-500 to-purple-500 text-white",
    secondary: "bg-gradient-to-r from-gray-100 to-gray-200 text-gray-900 dark:from-gray-700 dark:to-gray-600 dark:text-white",
    success: "bg-gradient-to-r from-green-500 to-emerald-500 text-white",
    warning: "bg-gradient-to-r from-yellow-500 to-orange-500 text-white",
    error: "bg-gradient-to-r from-red-500 to-pink-500 text-white",
    magic: "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white"
  }

  return (
    <motion.span
      ref={ref}
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium shadow-sm",
        variants[variant],
        glow && "shadow-lg",
        className
      )}
      animate={pulse ? { scale: [1, 1.05, 1] } : {}}
      transition={pulse ? { duration: 2, repeat: Infinity } : {}}
      whileHover={{ scale: 1.05 }}
      {...props}
    >
      {children}
    </motion.span>
  )
})

MagicBadge.displayName = "MagicBadge"

/**
 * Magic UI Separator with gradient effects
 */
export const MagicSeparator = React.forwardRef(({ 
  className, 
  orientation = "horizontal",
  gradient = false,
  ...props 
}, ref) => {
  return (
    <motion.div
      ref={ref}
      className={cn(
        "shrink-0",
        orientation === "horizontal" 
          ? gradient 
            ? "h-px w-full bg-gradient-to-r from-transparent via-gray-300 to-transparent dark:via-gray-700"
            : "h-px w-full bg-gray-200 dark:bg-gray-800"
          : gradient
            ? "w-px h-full bg-gradient-to-b from-transparent via-gray-300 to-transparent dark:via-gray-700"
            : "w-px h-full bg-gray-200 dark:bg-gray-800",
        className
      )}
      initial={{ scaleX: orientation === "horizontal" ? 0 : 1, scaleY: orientation === "vertical" ? 0 : 1 }}
      animate={{ scaleX: 1, scaleY: 1 }}
      transition={{ duration: 0.5 }}
      {...props}
    />
  )
})

MagicSeparator.displayName = "MagicSeparator"

/**
 * Magic UI Skeleton with shimmer effect
 */
export const MagicSkeleton = ({ className, ...props }) => {
  return (
    <motion.div
      className={cn(
        "relative overflow-hidden rounded-md bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800",
        className
      )}
      {...props}
    >
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent dark:via-gray-600/50"
        initial={{ x: "-100%" }}
        animate={{ x: "100%" }}
        transition={{
          repeat: Infinity,
          duration: 1.5,
          ease: "linear"
        }}
      />
    </motion.div>
  )
}

/**
 * Magic UI Tooltip with animations
 */
export const MagicTooltip = ({ 
  children, 
  content, 
  side = "top",
  className,
  ...props 
}) => {
  const [open, setOpen] = React.useState(false)

  const sideClasses = {
    top: "bottom-full left-1/2 transform -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 transform -translate-x-1/2 mt-2",
    left: "right-full top-1/2 transform -translate-y-1/2 mr-2",
    right: "left-full top-1/2 transform -translate-y-1/2 ml-2"
  }

  return (
    <div 
      className="relative inline-block"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      {...props}
    >
      {children}
      
      <AnimatePresence>
        {open && (
          <motion.div
            className={cn(
              "absolute z-50 px-3 py-2 text-sm text-white bg-gray-900 dark:bg-gray-700 rounded-lg shadow-lg whitespace-nowrap",
              sideClasses[side],
              className
            )}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.15 }}
          >
            {content}
            <div className="absolute w-2 h-2 bg-gray-900 dark:bg-gray-700 transform rotate-45" 
                 style={{
                   [side === 'top' ? 'top' : side === 'bottom' ? 'bottom' : side === 'left' ? 'right' : 'left']: 
                   side === 'top' || side === 'bottom' ? 'calc(100% - 4px)' : '50%',
                   [side === 'top' || side === 'bottom' ? 'left' : 'top']: '50%',
                   transform: 'translate(-50%, -50%) rotate(45deg)'
                 }} 
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default { MagicAvatar, MagicBadge, MagicSeparator, MagicSkeleton, MagicTooltip }
