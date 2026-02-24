import * as React from "react"
import { cn } from "@components/web/lib/utils"

const Header = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <header
      ref={ref}
      className={cn(
        "sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60",
        className
      )}
      {...props}
    />
  )
)
Header.displayName = "Header"

const HeaderContainer = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex h-14 max-w-full items-center justify-between px-4 sm:px-6 lg:px-8", className)}
      {...props}
    />
  )
)
HeaderContainer.displayName = "HeaderContainer"

const HeaderLeft = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center gap-4", className)} {...props} />
  )
)
HeaderLeft.displayName = "HeaderLeft"

const HeaderRight = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center gap-2", className)} {...props} />
  )
)
HeaderRight.displayName = "HeaderRight"

const HeaderBrand = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("text-lg font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
)
HeaderBrand.displayName = "HeaderBrand"

export {
  Header,
  HeaderContainer,
  HeaderLeft,
  HeaderRight,
  HeaderBrand,
}
