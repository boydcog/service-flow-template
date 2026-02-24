import React, { forwardRef } from "react"
import {
  Checkbox as GluestackCheckbox,
  CheckboxIcon,
  CheckboxLabel,
  CheckIcon,
  HStack,
} from "@gluestack-ui/themed"

export interface CheckboxProps
  extends React.ComponentPropsWithoutRef<typeof GluestackCheckbox> {
  label?: string
}

/**
 * Checkbox component for React Native with Gluestack
 * Props match Web Checkbox API for consistency
 */
const Checkbox = forwardRef<React.ElementRef<typeof GluestackCheckbox>, CheckboxProps>(
  ({ label, value, ...props }, ref) => (
    <HStack gap="$2" alignItems="center">
      <GluestackCheckbox
        ref={ref}
        value={value}
        {...props}
      >
        <CheckboxIcon as={CheckIcon} strokeWidth={3} size="sm" />
      </GluestackCheckbox>
      {label && (
        <CheckboxLabel
          size="sm"
          fontWeight="$medium"
        >
          {label}
        </CheckboxLabel>
      )}
    </HStack>
  )
)
Checkbox.displayName = "Checkbox"

export { Checkbox, CheckboxIcon, CheckboxLabel }
