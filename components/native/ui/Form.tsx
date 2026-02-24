import React, { forwardRef } from "react"
import { VStack, FormControl, FormControlLabel, FormControlLabelText, FormControlHelper, FormControlHelperText, FormControlError, FormControlErrorIcon, FormControlErrorText, AlertCircleIcon } from "@gluestack-ui/themed"

/**
 * Form component for React Native with Gluestack
 * Props match Web Form API for consistency
 */
const Form = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack ref={ref} gap="$4" {...props}>
      {children}
    </VStack>
  )
)
Form.displayName = "Form"

const FormItem = forwardRef<React.ElementRef<typeof FormControl>, React.ComponentPropsWithoutRef<typeof FormControl>>(
  ({ children, ...props }, ref) => (
    <FormControl ref={ref} {...props}>
      {children}
    </FormControl>
  )
)
FormItem.displayName = "FormItem"

const FormLabel = forwardRef<React.ElementRef<typeof FormControlLabel>, React.ComponentPropsWithoutRef<typeof FormControlLabel>>(
  ({ children, ...props }, ref) => (
    <FormControlLabel ref={ref} {...props}>
      <FormControlLabelText>{children}</FormControlLabelText>
    </FormControlLabel>
  )
)
FormLabel.displayName = "FormLabel"

const FormDescription = forwardRef<React.ElementRef<typeof FormControlHelper>, React.ComponentPropsWithoutRef<typeof FormControlHelper>>(
  ({ children, ...props }, ref) => (
    <FormControlHelper ref={ref} {...props}>
      <FormControlHelperText size="sm">{children}</FormControlHelperText>
    </FormControlHelper>
  )
)
FormDescription.displayName = "FormDescription"

const FormMessage = forwardRef<React.ElementRef<typeof FormControlError>, React.ComponentPropsWithoutRef<typeof FormControlError>>(
  ({ children, ...props }, ref) => (
    <FormControlError ref={ref} {...props}>
      <FormControlErrorIcon as={AlertCircleIcon} />
      <FormControlErrorText>{children}</FormControlErrorText>
    </FormControlError>
  )
)
FormMessage.displayName = "FormMessage"

export { Form, FormItem, FormLabel, FormDescription, FormMessage }
