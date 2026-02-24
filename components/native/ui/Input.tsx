import React, { forwardRef } from "react"
import {
  Input as GluestackInput,
  InputIcon,
  InputSlot,
  InputField,
} from "@gluestack-ui/themed"

export interface InputProps
  extends React.ComponentPropsWithoutRef<typeof GluestackInputField> {
  error?: boolean
}

/**
 * Input component for React Native with Gluestack
 * Props match Web Input API for consistency
 */
const Input = forwardRef<React.ElementRef<typeof GluestackInputField>, InputProps>(
  ({ error = false, ...props }, ref) => (
    <GluestackInput isInvalid={error}>
      <InputField ref={ref} {...props} />
    </GluestackInput>
  )
)

Input.displayName = "Input"

export { Input, InputIcon, InputSlot, InputField }
