import React, { forwardRef } from "react"
import { Box, HStack, Text } from "@gluestack-ui/themed"

/**
 * Header component for React Native with Gluestack
 * Props match Web Header API for consistency
 */
const Header = forwardRef<React.ElementRef<typeof Box>, React.ComponentPropsWithoutRef<typeof Box>>(
  ({ children, ...props }, ref) => (
    <Box
      ref={ref}
      bg="$background"
      borderBottomWidth={1}
      borderBottomColor="$border"
      px="$4"
      py="$3"
      {...props}
    >
      {children}
    </Box>
  )
)
Header.displayName = "Header"

const HeaderContainer = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack
      ref={ref}
      justifyContent="space-between"
      alignItems="center"
      gap="$4"
      {...props}
    >
      {children}
    </HStack>
  )
)
HeaderContainer.displayName = "HeaderContainer"

const HeaderLeft = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack ref={ref} alignItems="center" gap="$4" {...props}>
      {children}
    </HStack>
  )
)
HeaderLeft.displayName = "HeaderLeft"

const HeaderRight = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack ref={ref} alignItems="center" gap="$2" {...props}>
      {children}
    </HStack>
  )
)
HeaderRight.displayName = "HeaderRight"

const HeaderBrand = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$lg"
      fontWeight="$semibold"
      {...props}
    >
      {children}
    </Text>
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
