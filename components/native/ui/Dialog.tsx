import React, { forwardRef } from "react"
import {
  Modal,
  ModalBackdrop,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Heading,
  Text,
  Icon,
  CloseIcon,
  VStack,
} from "@gluestack-ui/themed"

/**
 * Dialog component for React Native with Gluestack
 * Props match Web Dialog API for consistency
 */
const Dialog = forwardRef<React.ElementRef<typeof Modal>, React.ComponentPropsWithoutRef<typeof Modal>>(
  ({ children, ...props }, ref) => (
    <Modal ref={ref} {...props}>
      {children}
    </Modal>
  )
)
Dialog.displayName = "Dialog"

const DialogTrigger = forwardRef<React.ElementRef<typeof VStack>, React.ComponentPropsWithoutRef<typeof VStack>>(
  ({ children, ...props }, ref) => (
    <VStack ref={ref} {...props}>
      {children}
    </VStack>
  )
)
DialogTrigger.displayName = "DialogTrigger"

const DialogContent = forwardRef<React.ElementRef<typeof ModalContent>, React.ComponentPropsWithoutRef<typeof ModalContent>>(
  ({ children, ...props }, ref) => (
    <>
      <ModalBackdrop />
      <ModalContent ref={ref} {...props}>
        {children}
      </ModalContent>
    </>
  )
)
DialogContent.displayName = "DialogContent"

const DialogHeader = forwardRef<React.ElementRef<typeof ModalHeader>, React.ComponentPropsWithoutRef<typeof ModalHeader>>(
  ({ children, ...props }, ref) => (
    <ModalHeader ref={ref} {...props}>
      {children}
    </ModalHeader>
  )
)
DialogHeader.displayName = "DialogHeader"

const DialogCloseButton = forwardRef<React.ElementRef<typeof ModalCloseButton>, React.ComponentPropsWithoutRef<typeof ModalCloseButton>>(
  (props, ref) => (
    <ModalCloseButton ref={ref} {...props}>
      <Icon as={CloseIcon} />
    </ModalCloseButton>
  )
)
DialogCloseButton.displayName = "DialogCloseButton"

const DialogBody = forwardRef<React.ElementRef<typeof ModalBody>, React.ComponentPropsWithoutRef<typeof ModalBody>>(
  ({ children, ...props }, ref) => (
    <ModalBody ref={ref} {...props}>
      {children}
    </ModalBody>
  )
)
DialogBody.displayName = "DialogBody"

const DialogFooter = forwardRef<React.ElementRef<typeof ModalFooter>, React.ComponentPropsWithoutRef<typeof ModalFooter>>(
  ({ children, ...props }, ref) => (
    <ModalFooter ref={ref} {...props}>
      {children}
    </ModalFooter>
  )
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = forwardRef<React.ElementRef<typeof Heading>, React.ComponentPropsWithoutRef<typeof Heading>>(
  ({ children, ...props }, ref) => (
    <Heading ref={ref} size="lg" {...props}>
      {children}
    </Heading>
  )
)
DialogTitle.displayName = "DialogTitle"

const DialogDescription = forwardRef<React.ElementRef<typeof Text>, React.ComponentPropsWithoutRef<typeof Text>>(
  ({ children, ...props }, ref) => (
    <Text ref={ref} size="sm" {...props}>
      {children}
    </Text>
  )
)
DialogDescription.displayName = "DialogDescription"

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogCloseButton,
  DialogBody,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}
