import * as React from "react"
import { cn } from "@components/web/lib/utils"
import { Card } from "./card"

interface StatCardProps extends React.HTMLAttributes<HTMLDivElement> {
  label: string
  value: string | number
  change?: {
    value: number
    direction: 'up' | 'down'
  }
  icon?: React.ReactNode
  variant?: 'default' | 'colored'
}

const StatCard = React.forwardRef<HTMLDivElement, StatCardProps>(
  ({ label, value, change, icon, variant = 'default', className, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn('p-6', className)} {...props}>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-muted-foreground">{label}</p>
            <h3 className="mt-2 text-2xl font-bold tracking-tight">{value}</h3>
            {change && (
              <p className={cn(
                'mt-2 text-xs font-medium',
                change.direction === 'up' ? 'text-green-600' : 'text-red-600'
              )}>
                {change.direction === 'up' ? '↑' : '↓'} {Math.abs(change.value)}% from last month
              </p>
            )}
          </div>
          {icon && (
            <div className="ml-4">
              {icon}
            </div>
          )}
        </div>
      </Card>
    )
  }
)
StatCard.displayName = "StatCard"

export { StatCard, type StatCardProps }
