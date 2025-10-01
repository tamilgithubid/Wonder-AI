import React from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

/**
 * Magic UI Scroll Area with custom scrollbar styling
 */
export const MagicScrollArea = React.forwardRef(({ 
  className, 
  children,
  maxHeight = "400px",
  ...props 
}, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "relative overflow-hidden rounded-lg",
        className
      )}
      style={{ maxHeight }}
      {...props}
    >
      <div className="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 dark:hover:scrollbar-thumb-gray-500 transition-colors">
        {children}
      </div>
    </div>
  )
})

MagicScrollArea.displayName = "MagicScrollArea"

/**
 * Magic UI Progress Bar with gradient fill and animations
 */
export const MagicProgress = React.forwardRef(({ 
  className, 
  value = 0,
  max = 100,
  size = "default",
  variant = "default",
  animated = false,
  ...props 
}, ref) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const sizes = {
    sm: "h-2",
    default: "h-3",
    lg: "h-4"
  }

  const variants = {
    default: "from-blue-500 to-purple-500",
    success: "from-green-500 to-emerald-500",
    warning: "from-yellow-500 to-orange-500",
    error: "from-red-500 to-pink-500"
  }

  return (
    <div
      ref={ref}
      className={cn(
        "relative w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700",
        sizes[size],
        className
      )}
      {...props}
    >
      <motion.div
        className={cn(
          "h-full rounded-full bg-gradient-to-r",
          variants[variant],
          animated && "bg-gradient-to-r animate-pulse"
        )}
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />
      
      {animated && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
          animate={{ x: ["-100%", "100%"] }}
          transition={{
            repeat: Infinity,
            duration: 1.5,
            ease: "linear"
          }}
        />
      )}
    </div>
  )
})

MagicProgress.displayName = "MagicProgress"

/**
 * Magic UI Switch with smooth toggle animation
 */
export const MagicSwitch = React.forwardRef(({ 
  className, 
  checked = false,
  onCheckedChange,
  disabled = false,
  size = "default",
  ...props 
}, ref) => {
  const sizes = {
    sm: { container: "w-8 h-4", thumb: "w-3 h-3" },
    default: { container: "w-11 h-6", thumb: "w-5 h-5" },
    lg: { container: "w-14 h-7", thumb: "w-6 h-6" }
  }

  return (
    <motion.button
      ref={ref}
      className={cn(
        "relative inline-flex items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
        sizes[size].container,
        checked 
          ? "bg-gradient-to-r from-blue-500 to-purple-500" 
          : "bg-gray-200 dark:bg-gray-700",
        disabled && "opacity-50 cursor-not-allowed",
        className
      )}
      onClick={() => !disabled && onCheckedChange?.(!checked)}
      disabled={disabled}
      whileTap={!disabled ? { scale: 0.95 } : {}}
      {...props}
    >
      <motion.div
        className={cn(
          "rounded-full bg-white shadow-lg",
          sizes[size].thumb
        )}
        animate={{
          x: checked ? `calc(100% + 2px)` : "2px"
        }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
      />
    </motion.button>
  )
})

MagicSwitch.displayName = "MagicSwitch"

/**
 * Magic UI Slider with gradient track and animated thumb
 */
export const MagicSlider = React.forwardRef(({ 
  className, 
  value = [0],
  onValueChange,
  max = 100,
  min = 0,
  step = 1,
  disabled = false,
  ...props 
}, ref) => {
  const percentage = ((value[0] - min) / (max - min)) * 100

  return (
    <div
      ref={ref}
      className={cn(
        "relative flex w-full touch-none select-none items-center",
        disabled && "opacity-50 cursor-not-allowed",
        className
      )}
      {...props}
    >
      {/* Track */}
      <div className="relative h-2 w-full grow overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
        {/* Filled track */}
        <motion.div
          className="absolute h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
          style={{ width: `${percentage}%` }}
          transition={{ duration: 0.1 }}
        />
      </div>
      
      {/* Thumb */}
      <motion.div
        className="absolute w-5 h-5 bg-white border-2 border-blue-500 rounded-full shadow-lg cursor-pointer"
        style={{ left: `calc(${percentage}% - 10px)` }}
        whileHover={!disabled ? { scale: 1.1 } : {}}
        whileDrag={{ scale: 1.2 }}
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        dragElastic={0}
        onDrag={(_, info) => {
          if (disabled) return
          const rect = ref.current?.getBoundingClientRect()
          if (!rect) return
          
          const newValue = Math.min(Math.max(
            min + ((info.point.x - rect.left) / rect.width) * (max - min), 
            min
          ), max)
          
          onValueChange?.([Math.round(newValue / step) * step])
        }}
      />
    </div>
  )
})

MagicSlider.displayName = "MagicSlider"

/**
 * Magic UI Alert with gradient borders and icons
 */
export const MagicAlert = React.forwardRef(({ 
  className, 
  children,
  variant = "default",
  ...props 
}, ref) => {
  const variants = {
    default: "border-blue-200 bg-blue-50 text-blue-900 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-100",
    success: "border-green-200 bg-green-50 text-green-900 dark:border-green-800 dark:bg-green-950 dark:text-green-100",
    warning: "border-yellow-200 bg-yellow-50 text-yellow-900 dark:border-yellow-800 dark:bg-yellow-950 dark:text-yellow-100",
    error: "border-red-200 bg-red-50 text-red-900 dark:border-red-800 dark:bg-red-950 dark:text-red-100"
  }

  return (
    <motion.div
      ref={ref}
      className={cn(
        "relative w-full rounded-lg border px-4 py-3 text-sm",
        variants[variant],
        className
      )}
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      {...props}
    >
      {children}
    </motion.div>
  )
})

MagicAlert.displayName = "MagicAlert"

export default { 
  MagicScrollArea, 
  MagicProgress, 
  MagicSwitch, 
  MagicSlider, 
  MagicAlert 
}
