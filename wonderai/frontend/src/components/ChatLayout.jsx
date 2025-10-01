import React, { useCallback, useMemo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
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

    // Mobile sidebar component
    const MobileSidebar = React.memo(() => (
        <Sheet>
            <SheetTrigger asChild>
                <Button
                    variant="ghost"
                    size="icon"
                    className="md:hidden"
                    aria-label="Open sidebar"
                >
                    <Menu className="h-5 w-5" />
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="p-0">
                <Sidebar isMobile={true} />
            </SheetContent>
        </Sheet>
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
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={handleToggleSidebar}
                            className="hidden md:flex"
                            aria-label="Toggle sidebar"
                        >
                            <Menu className="h-5 w-5" />
                        </Button>

                        {/* Logo and Title */}
                        <div className="flex items-center gap-2">
                            <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
                                <Bot className="h-5 w-5 text-primary-foreground" />
                            </div>
                            <h1 className="text-lg font-semibold">WonderAI</h1>
                        </div>

                        {/* Connection Status */}
                        <Badge
                            variant={isConnected ? 'default' : 'secondary'}
                            className="hidden sm:inline-flex"
                        >
                            {isConnected ? 'Connected' : 'Disconnected'}
                        </Badge>
                    </div>

                    {/* Navigation */}
                    <nav className="flex items-center gap-1">
                        {navigationItems.map((item) => {
                            const IconComponent = item.icon
                            return (
                                <Button
                                    key={item.id}
                                    variant={item.active ? 'default' : 'ghost'}
                                    size="sm"
                                    onClick={() => handleViewChange(item.id)}
                                    className="gap-2"
                                    aria-pressed={item.active}
                                >
                                    <IconComponent className="h-4 w-4" />
                                    <span className="hidden sm:inline">{item.label}</span>
                                </Button>
                            )
                        })}

                        <Separator orientation="vertical" className="h-6 mx-2" />

                        <Button variant="ghost" size="icon" aria-label="Settings">
                            <Settings className="h-4 w-4" />
                        </Button>
                    </nav>
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
