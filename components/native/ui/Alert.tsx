import React, { forwardRef } from "react"
import {
  Box,
  Text,
} from "@gluestack-ui/themed"

export interface AlertProps extends React.ComponentPropsWithoutRef<typeof Box> {
  variant?: "default" | "destructive" | "warning" | "success"
}

/**
 * Alert component for React Native with Gluestack
 * Props match Web Alert API for consistency
 */
const Alert = forwardRef<React.ElementRef<typeof Box>, AlertProps>(
  ({ variant = "default", children, ...props }, ref) => {
    const getVariantStyles = () => {
      switch (variant) {
        case "destructive":
          return { borderColor: "$destructive", bg: "$red50" }
        case "warning":
          return { borderColor: "$yellow600", bg: "$yellow50" }
        case "success":
          return { borderColor: "$green600", bg: "$green50" }
        default:
          return { borderColor: "$border", bg: "$background" }
      }
    }

    return (
      <Box
        ref={ref}
        borderWidth={1}
        borderRadius="$md"
        p="$4"
        {...getVariantStyles()}
        {...props}
      >
        {children}
      </Box>
    )
  }
)
Alert.displayName = "Alert"

const AlertTitle = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$base"
      fontWeight="$medium"
      mb="$1"
      {...props}
    >
      {children}
    </Text>
  )
)
AlertTitle.displayName = "AlertTitle"

const AlertDescription = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$sm"
      lineHeight="$relaxed"
      {...props}
    >
      {children}
    </Text>
  )
)
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }
