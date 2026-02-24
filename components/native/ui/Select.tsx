import React, { forwardRef } from "react"
import {
  Select as GluestackSelect,
  SelectTrigger,
  SelectInput,
  SelectIcon,
  SelectPortal,
  SelectBackdrop,
  SelectContent,
  SelectDragIndicator,
  SelectItem,
  ChevronDownIcon,
} from "@gluestack-ui/themed"

export interface SelectProps
  extends React.ComponentPropsWithoutRef<typeof SelectTrigger> {
  placeholder?: string
  options?: Array<{ label: string; value: string }>
}

/**
 * Select component for React Native with Gluestack
 * Props match Web Select API for consistency
 */
const Select = forwardRef<React.ElementRef<typeof GluestackSelect>, SelectProps>(
  ({ placeholder, options = [], children, ...props }, ref) => (
    <GluestackSelect {...props} ref={ref}>
      <SelectTrigger>
        <SelectInput placeholder={placeholder} />
        <SelectIcon as={ChevronDownIcon} />
      </SelectTrigger>
      <SelectPortal>
        <SelectBackdrop />
        <SelectContent>
          <SelectDragIndicator />
          {options.map((option) => (
            <SelectItem
              key={option.value}
              label={option.label}
              value={option.value}
            />
          ))}
          {children}
        </SelectContent>
      </SelectPortal>
    </GluestackSelect>
  )
)
Select.displayName = "Select"

export {
  Select,
  SelectTrigger,
  SelectInput,
  SelectIcon,
  SelectPortal,
  SelectBackdrop,
  SelectContent,
  SelectDragIndicator,
  SelectItem,
}
