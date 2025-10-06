import React, { useCallback, useMemo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
    MagicButton,
    MagicBadge,
    MagicSeparator,
    MagicNav,
    MagicNavItem,
    MagicDialog
} from '@/components/magicui'
import { ChatInterface } from './ChatInterface'
import { Sidebar } from './Sidebar'
import { HealthCheck } from './HealthCheck'
import {
    selectIsConnected,
    selectCurrentView,
    selectIsSidebarOpen,
    toggleSidebar,
    setCurrentView
} from '@/store/chatSlice'
import {
    MessageSquare,
    Image as ImageIcon,
    Map,
    Menu,
    Settings,
    Bot
} from 'lucide-react'

/**
 * Main layout component for the WonderAI chat application
 * Uses React 19 patterns and modern UI design
 */
export const ChatLayout = React.memo(() => {
    const dispatch = useDispatch()
    const isConnected = useSelector(selectIsConnected)
    const currentView = useSelector(selectCurrentView)
    const isSidebarOpen = useSelector(selectIsSidebarOpen)

    // Navigation items with icons and labels
    const navigationItems = useMemo(() => [
        {
            id: 'chat',
            label: 'Chat',
            icon: MessageSquare,
            active: currentView === 'chat',
        },
        {
            id: 'images',
            label: 'Images',
            icon: ImageIcon,
            active: currentView === 'images',
        },
        {
            id: 'maps',
            label: 'Maps',
            icon: Map,
            active: currentView === 'maps',
        },
    ], [currentView])

    // Memoized handlers for performance
    const handleViewChange = useCallback((view) => {
        dispatch(setCurrentView(view))
    }, [dispatch])

    const handleToggleSidebar = useCallback(() => {
        dispatch(toggleSidebar())
    }, [dispatch])

    // Mobile sidebar state
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = React.useState(false)

    // Mobile sidebar component
    const MobileSidebar = React.memo(() => (
        <>
            <MagicButton
                variant="ghost"
                size="icon"
                className="md:hidden"
                onClick={() => setIsMobileSidebarOpen(true)}
                aria-label="Open sidebar"
            >
                <Menu className="h-5 w-5" />
            </MagicButton>
            <MagicDialog
                open={isMobileSidebarOpen}
                onClose={() => setIsMobileSidebarOpen(false)}
                size="sm"
                className="p-0 max-w-xs"
            >
                <Sidebar isMobile={true} />
            </MagicDialog>
        </>
    ))

    return (
        <div className="flex h-screen bg-background">
            {/* Desktop Sidebar */}
            <aside className={`
        hidden md:flex md:flex-col md:w-64 
        border-r bg-card
        transition-all duration-300 ease-in-out
        ${isSidebarOpen ? 'md:translate-x-0' : 'md:-translate-x-full md:w-0'}
      `}>
                <Sidebar />
            </aside>

            {/* Main Content Area */}
            <div className="flex flex-col flex-1 overflow-hidden">
                {/* Header */}
                <header className="flex items-center justify-between p-4 border-b bg-card">
                    <div className="flex items-center gap-3">
                        {/* Mobile Menu Button */}
                        <MobileSidebar />

                        {/* Desktop Sidebar Toggle */}
                        <MagicButton
                            variant="ghost"
                            size="icon"
                            onClick={handleToggleSidebar}
                            className="hidden md:flex"
                            aria-label="Toggle sidebar"
                        >
                            <Menu className="h-5 w-5" />
                        </MagicButton>

                        {/* Logo and Title */}
                        <div className="flex items-center gap-2">
                            <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
                                <Bot className="h-5 w-5 text-primary-foreground" />
                            </div>
                            <h1 className="text-lg font-semibold">WonderAI</h1>
                        </div>

                        {/* Connection Status */}
                        <MagicBadge
                            variant={isConnected ? 'success' : 'secondary'}
                            className="hidden sm:inline-flex"
                            pulse={isConnected}
                            glow={isConnected}
                        >
                            {isConnected ? 'Connected' : 'Disconnected'}
                        </MagicBadge>
                    </div>

                    {/* Navigation */}
                    <MagicNav className="flex items-center gap-1">
                        {navigationItems.map((item) => {
                            const IconComponent = item.icon
                            return (
                                <MagicNavItem
                                    key={item.id}
                                    active={item.active}
                                    onClick={() => handleViewChange(item.id)}
                                    className="gap-2"
                                >
                                    <IconComponent className="h-4 w-4" />
                                    <span className="hidden sm:inline">{item.label}</span>
                                </MagicNavItem>
                            )
                        })}

                        <MagicSeparator orientation="vertical" className="h-6 mx-2" gradient />

                        <MagicButton variant="ghost" size="icon" aria-label="Settings">
                            <Settings className="h-4 w-4" />
                        </MagicButton>
                    </MagicNav>
                </header>

                {/* Health Check Status */}
                <div className="p-4">
                    <HealthCheck />
                </div>

                {/* Main Content */}
                <main className="flex-1 overflow-hidden">
                    <ChatInterface />
                </main>
            </div>
        </div>
    )
})

ChatLayout.displayName = 'ChatLayout'
