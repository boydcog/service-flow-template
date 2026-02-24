import React, { forwardRef } from "react"
import { VStack, Pressable, Box } from "@gluestack-ui/themed"

/**
 * Sidebar component for React Native with Gluestack
 * Props match Web Sidebar API for consistency
 */
const Sidebar = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack
      ref={ref}
      h="100%"
      w={64}
      bg="$sidebarBackground"
      borderRightWidth={1}
      borderRightColor="$sidebarBorder"
      {...props}
    >
      {children}
    </VStack>
  )
)
Sidebar.displayName = "Sidebar"

const SidebarContent = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack
      ref={ref}
      flex={1}
      px="$4"
      py="$4"
      overflowY="auto"
      {...props}
    >
      {children}
    </VStack>
  )
)
SidebarContent.displayName = "SidebarContent"

const SidebarHeader = forwardRef<React.ElementRef<typeof Box>, React.ComponentPropsWithoutRef<typeof Box>>(
  ({ children, ...props }, ref) => (
    <Box
      ref={ref}
      borderBottomWidth={1}
      borderBottomColor="$sidebarBorder"
      px="$4"
      py="$3"
      {...props}
    >
      {children}
    </Box>
  )
)
SidebarHeader.displayName = "SidebarHeader"

const SidebarFooter = forwardRef<React.ElementRef<typeof Box>, React.ComponentPropsWithoutRef<typeof Box>>(
  ({ children, ...props }, ref) => (
    <Box
      ref={ref}
      borderTopWidth={1}
      borderTopColor="$sidebarBorder"
      px="$4"
      py="$3"
      mt="auto"
      {...props}
    >
      {children}
    </Box>
  )
)
SidebarFooter.displayName = "SidebarFooter"

const SidebarItem = forwardRef<React.ElementRef<typeof Pressable>, React.ComponentPropsWithoutRef<typeof Pressable>>(
  ({ children, ...props }, ref) => (
    <Pressable
      ref={ref}
      px="$3"
      py="$2"
      rounded="$md"
      {...props}
    >
      {children}
    </Pressable>
  )
)
SidebarItem.displayName = "SidebarItem"

const SidebarToggle = forwardRef<React.ElementRef<typeof Pressable>, React.ComponentPropsWithoutRef<typeof Pressable>>(
  ({ children, ...props }, ref) => (
    <Pressable
      ref={ref}
      display="flex"
      lg={{ display: "none" }}
      p="$2"
      {...props}
    >
      {children}
    </Pressable>
  )
)
SidebarToggle.displayName = "SidebarToggle"

export {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarItem,
  SidebarToggle,
}
