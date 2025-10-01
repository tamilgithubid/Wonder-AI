import React from 'react'
import { useGetHealthQuery } from '@/store'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

/**
 * Simple health check component to test backend connectivity
 */
export const HealthCheck = React.memo(() => {
    const { data: health, error, isLoading } = useGetHealthQuery()

    if (isLoading) {
        return (
            <Card className="p-4">
                <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Checking backend connection...</span>
                </div>
            </Card>
        )
    }

    if (error) {
        return (
            <Card className="p-4 border-destructive">
                <div className="flex items-center gap-2">
                    <XCircle className="w-4 h-4 text-destructive" />
                    <span className="text-destructive">Backend connection failed</span>
                    <Badge variant="destructive">Offline</Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                    Error: {error.message || 'Unknown error'}
                </p>
            </Card>
        )
    }

    return (
        <Card className="p-4 border-green-200 bg-green-50">
            <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span className="text-green-800">Backend connected successfully</span>
                <Badge className="bg-green-100 text-green-800">
                    {health?.status || 'Online'}
                </Badge>
            </div>
            {health?.timestamp && (
                <p className="text-sm text-green-600 mt-2">
                    Last check: {new Date(health.timestamp).toLocaleTimeString()}
                </p>
            )}
        </Card>
    )
})

HealthCheck.displayName = 'HealthCheck'
