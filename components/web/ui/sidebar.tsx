import * as React from "react"
import { Menu } from "lucide-react"
import { cn } from "@components/web/lib/utils"

const Sidebar = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    collapsible?: boolean
  }
>(({ className, ...props }, ref) => (
  <aside
    ref={ref}
    className={cn(
      "fixed left-0 top-0 z-40 h-screen w-64 border-r border-sidebar-border bg-sidebar-background",
      "hidden lg:flex flex-col",
      className
    )}
    {...props}
  />
))
Sidebar.displayName = "Sidebar"

const SidebarContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex-1 overflow-y-auto px-4 py-4", className)}
      {...props}
    />
  )
)
SidebarContent.displayName = "SidebarContent"

const SidebarHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("border-b border-sidebar-border px-4 py-3", className)}
      {...props}
    />
  )
)
SidebarHeader.displayName = "SidebarHeader"

const SidebarFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("border-t border-sidebar-border px-4 py-3 mt-auto", className)}
      {...props}
    />
  )
)
SidebarFooter.displayName = "SidebarFooter"

const SidebarItem = React.forwardRef<
  HTMLAnchorElement,
  React.AnchorHTMLAttributes<HTMLAnchorElement>
>(({ className, ...props }, ref) => (
  <a
    ref={ref}
    className={cn(
      "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors hover:bg-sidebar-accent/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sidebar-accent data-[active]:bg-sidebar-accent data-[active]:text-sidebar-background",
      className
    )}
    {...props}
  />
))
SidebarItem.displayName = "SidebarItem"

const SidebarToggle = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex lg:hidden items-center justify-center rounded-md p-2 text-foreground hover:bg-accent",
        className
      )}
      {...props}
    >
      <Menu className="h-5 w-5" />
    </button>
  )
)
SidebarToggle.displayName = "SidebarToggle"

// Mobile sidebar (simplified, without Sheet primitive)
const MobileSidebar = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  (props, ref) => <div ref={ref} {...props} />
)
MobileSidebar.displayName = "MobileSidebar"

const MobileSidebarTrigger = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  (props, ref) => <button ref={ref} {...props} />
)
MobileSidebarTrigger.displayName = "MobileSidebarTrigger"

const MobileSidebarContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "fixed inset-y-0 left-0 z-40 w-64 border-r border-sidebar-border bg-sidebar-background p-0",
        className
      )}
      {...props}
    />
  )
)
MobileSidebarContent.displayName = "MobileSidebarContent"

export {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarItem,
  SidebarToggle,
  MobileSidebar,
  MobileSidebarTrigger,
  MobileSidebarContent,
}
