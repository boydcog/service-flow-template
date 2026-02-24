import * as React from "react"
import { cn } from "@components/web/lib/utils"
import { Card } from "./card"
import { Button } from "./button"
import { Badge } from "./badge"

interface Feature {
  name: string
  included: boolean
}

interface PricingCardProps extends React.HTMLAttributes<HTMLDivElement> {
  name: string
  price: string
  description?: string
  features: Feature[]
  cta?: string
  featured?: boolean
  badge?: string
}

const PricingCard = React.forwardRef<HTMLDivElement, PricingCardProps>(
  ({
    name,
    price,
    description,
    features,
    cta = 'Get Started',
    featured = false,
    badge,
    className,
    ...props
  }, ref) => {
    return (
      <Card
        ref={ref}
        className={cn(
          'relative p-8 flex flex-col',
          featured && 'ring-2 ring-primary shadow-lg scale-105',
          className
        )}
        {...props}
      >
        {badge && (
          <Badge className="mb-4 w-fit">{badge}</Badge>
        )}

        <div className="mb-6">
          <h3 className="text-2xl font-bold">{name}</h3>
          {description && (
            <p className="text-sm text-muted-foreground mt-1">{description}</p>
          )}
        </div>

        <div className="mb-6">
          <span className="text-4xl font-bold">${price}</span>
          <span className="text-muted-foreground ml-1">/month</span>
        </div>

        <Button
          className="mb-6 w-full"
          variant={featured ? 'default' : 'outline'}
        >
          {cta}
        </Button>

        <div className="space-y-3 flex-1">
          <p className="text-xs font-medium text-muted-foreground">FEATURES</p>
          {features.map((feature, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className={cn(
                'text-lg leading-none mt-0.5',
                feature.included ? 'text-green-600' : 'text-muted-foreground'
              )}>
                {feature.included ? '✓' : '×'}
              </span>
              <span className={cn(
                'text-sm',
                !feature.included && 'text-muted-foreground'
              )}>
                {feature.name}
              </span>
            </div>
          ))}
        </div>
      </Card>
    )
  }
)
PricingCard.displayName = "PricingCard"

export { PricingCard, type PricingCardProps, type Feature }
