import React, { forwardRef } from "react"
import { Toast, VStack, Text, Pressable, CloseIcon, Icon } from "@gluestack-ui/themed"

/**
 * Toast component for React Native with Gluestack
 * Props match Web Toast API for consistency
 */
const Toast = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack> & {
  variant?: "default" | "destructive"
}>(
  ({ variant = "default", children, ...props }, ref) => {
    const getBgColor = () => {
      return variant === "destructive" ? "$destructive" : "$background"
    }

    return (
      <VStack
        ref={ref}
        bg={getBgColor()}
        borderWidth={1}
        borderColor="$border"
        p="$6"
        pr="$8"
        rounded="$md"
        gap="$4"
        {...props}
      >
        {children}
      </VStack>
    )
  }
)
Toast.displayName = "Toast"

const ToastTitle = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$sm"
      fontWeight="$semibold"
      {...props}
    >
      {children}
    </Text>
  )
)
ToastTitle.displayName = "ToastTitle"

const ToastDescription = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text
      ref={ref}
      fontSize="$sm"
      opacity={0.9}
      {...props}
    >
      {children}
    </Text>
  )
)
ToastDescription.displayName = "ToastDescription"

const ToastClose = forwardRef<React.ElementRef<typeof Pressable>, React.ComponentPropsWithoutRef<typeof Pressable>>(
  (props, ref) => (
    <Pressable
      ref={ref}
      position="absolute"
      right="$2"
      top="$2"
      p="$1"
      {...props}
    >
      <Icon as={CloseIcon} size="md" />
    </Pressable>
  )
)
ToastClose.displayName = "ToastClose"

const ToastAction = forwardRef<React.ElementRef<typeof Pressable>, React.ComponentPropsWithoutRef<typeof Pressable>>(
  (props, ref) => (
    <Pressable ref={ref} {...props} />
  )
)
ToastAction.displayName = "ToastAction"

export {
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastAction,
}
