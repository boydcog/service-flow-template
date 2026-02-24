import React, { forwardRef } from "react"
import { HStack, Pressable } from "@gluestack-ui/themed"

/**
 * Navbar component for React Native with Gluestack
 * Props match Web Navbar API for consistency
 */
const Navbar = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack
      ref={ref}
      h="$14"
      alignItems="center"
      gap="$1"
      borderBottomWidth={1}
      borderBottomColor="$border"
      bg="$background"
      px="$4"
      {...props}
    >
      {children}
    </HStack>
  )
)
Navbar.displayName = "Navbar"

const NavbarItem = forwardRef<React.ElementRef<typeof Pressable>, React.ComponentPropsWithoutRef<typeof Pressable>>(
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
NavbarItem.displayName = "NavbarItem"

const NavbarMenu = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack ref={ref} alignItems="center" ml="auto" gap="$1" {...props}>
      {children}
    </HStack>
  )
)
NavbarMenu.displayName = "NavbarMenu"

const NavbarItemGroup = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack ref={ref} alignItems="center" {...props}>
      {children}
    </HStack>
  )
)
NavbarItemGroup.displayName = "NavbarItemGroup"

export {
  Navbar,
  NavbarItem,
  NavbarMenu,
  NavbarItemGroup,
}
