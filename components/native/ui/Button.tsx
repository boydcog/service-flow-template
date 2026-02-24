import React, { forwardRef } from "react"
import {
  Button as GluestackButton,
  ButtonText,
  ButtonIcon,
  ButtonGroup,
} from "@gluestack-ui/themed"
import { cva, type VariantProps } from "class-variance-authority"

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const buttonVariants = cva("", {
  variants: {
    variant: {
      default: "bg-primary",
      destructive: "bg-destructive",
      outline: "bg-transparent border border-input",
      secondary: "bg-secondary",
      ghost: "bg-transparent",
      link: "bg-transparent",
    },
    size: {
      default: "h-10 px-4",
      sm: "h-9 px-3",
      lg: "h-11 px-8",
      icon: "h-10 w-10",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "default",
  },
})

export interface ButtonProps
  extends React.ComponentPropsWithoutRef<typeof GluestackButton>,
    VariantProps<typeof buttonVariants> {
  children?: React.ReactNode
}

/**
 * Button component for React Native with Gluestack
 * Props match Web Button API for consistency
 */
const Button = forwardRef<React.ElementRef<typeof GluestackButton>, ButtonProps>(
  ({ variant = "default", size = "default", children, ...props }, ref) => {
    return (
      <GluestackButton
        ref={ref}
        action={variant === "destructive" ? "error" : "primary"}
        size={size === "default" ? "md" : size === "sm" ? "sm" : "lg"}
        {...props}
      >
        {typeof children === "string" ? (
          <ButtonText>{children}</ButtonText>
        ) : (
          children
        )}
      </GluestackButton>
    )
  }
)

Button.displayName = "Button"

export { Button, ButtonText, ButtonIcon, ButtonGroup }
