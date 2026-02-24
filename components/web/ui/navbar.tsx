import * as React from "react"
import { cn } from "@components/web/lib/utils"

const Navbar = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <nav
      ref={ref}
      className={cn(
        "flex h-14 items-center gap-1 border-b border-border bg-background px-4",
        className
      )}
      {...props}
    />
  )
)
Navbar.displayName = "Navbar"

const NavbarItem = React.forwardRef<HTMLAnchorElement, React.AnchorHTMLAttributes<HTMLAnchorElement>>(
  ({ className, ...props }, ref) => (
    <a
      ref={ref}
      className={cn(
        "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent data-[active]:text-accent-foreground",
        className
      )}
      {...props}
    />
  )
)
NavbarItem.displayName = "NavbarItem"

const NavbarMenu = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center gap-1 ml-auto", className)} {...props} />
  )
)
NavbarMenu.displayName = "NavbarMenu"

const NavbarItemGroup = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center", className)} {...props} />
  )
)
NavbarItemGroup.displayName = "NavbarItemGroup"

export {
  Navbar,
  NavbarItem,
  NavbarMenu,
  NavbarItemGroup,
}
