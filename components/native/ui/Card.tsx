import React, { forwardRef } from "react"
import {
  Box,
  VStack,
  HStack,
  Text,
} from "@gluestack-ui/themed"

/**
 * Card component for React Native with Gluestack
 * Provides same structure as Web Card components
 */
const Card = forwardRef<React.ElementRef<typeof Box>, React.ComponentPropsWithoutRef<typeof Box>>(
  ({ children, ...props }, ref) => (
    <Box
      ref={ref}
      bg="$card"
      borderWidth={1}
      borderColor="$border"
      borderRadius="$lg"
      p="$6"
      {...props}
    >
      {children}
    </Box>
  )
)
Card.displayName = "Card"

const CardHeader = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack ref={ref} gap="$1.5" pb="$0" {...props}>
      {children}
    </VStack>
  )
)
CardHeader.displayName = "CardHeader"

const CardContent = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack ref={ref} gap="$0" {...props}>
      {children}
    </VStack>
  )
)
CardContent.displayName = "CardContent"

const CardFooter = forwardRef<React.ElementRef<typeof HStack>, React.ComponentPropsWithoutRef<typeof HStack>>(
  ({ children, ...props }, ref) => (
    <HStack ref={ref} pt="$0" gap="$2" {...props}>
      {children}
    </HStack>
  )
)
CardFooter.displayName = "CardFooter"

const CardTitle = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$2xl"
      fontWeight="$semibold"
      lineHeight="$none"
      {...props}
    >
      {children}
    </Text>
  )
)
CardTitle.displayName = "CardTitle"

const CardDescription = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$sm"
      color="$mutedForeground"
      {...props}
    >
      {children}
    </Text>
  )
)
CardDescription.displayName = "CardDescription"

export {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
  CardDescription,
}
