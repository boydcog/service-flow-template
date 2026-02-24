import type { Meta, StoryObj } from '@storybook/react'
import { useEffect, useState } from 'react'
import { Toast, ToastAction, ToastClose, ToastDescription, ToastTitle, ToastProvider, ToastViewport } from './toast'
import { Button } from './button'

const meta = {
  title: 'Web/Toast',
  component: Toast,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  decorators: [
    (Story) => (
      <ToastProvider>
        <ToastViewport />
        <Story />
      </ToastProvider>
    ),
  ],
} satisfies Meta<typeof Toast>

export default meta
type Story = StoryObj<typeof meta>

function DefaultToastDemo() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    setOpen(true)
  }, [])

  return (
    <>
      <Button onClick={() => setOpen(true)}>Show Toast</Button>
      {open && (
        <Toast onOpenChange={setOpen}>
          <div className="grid gap-1">
            <ToastTitle>Success!</ToastTitle>
            <ToastDescription>Your action has been completed.</ToastDescription>
          </div>
          <ToastClose />
        </Toast>
      )}
    </>
  )
}

function DestructiveToastDemo() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    setOpen(true)
  }, [])

  return (
    <>
      <Button onClick={() => setOpen(true)}>Show Error Toast</Button>
      {open && (
        <Toast variant="destructive" onOpenChange={setOpen}>
          <div className="grid gap-1">
            <ToastTitle>Error!</ToastTitle>
            <ToastDescription>Something went wrong. Please try again.</ToastDescription>
          </div>
          <ToastClose />
        </Toast>
      )}
    </>
  )
}

function WithActionToastDemo() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    setOpen(true)
  }, [])

  return (
    <>
      <Button onClick={() => setOpen(true)}>Show Toast with Action</Button>
      {open && (
        <Toast onOpenChange={setOpen}>
          <div className="grid gap-1">
            <ToastTitle>Scheduled: Catch up</ToastTitle>
            <ToastDescription>Friday, February 10, 2025 at 5:57 PM</ToastDescription>
          </div>
          <ToastAction altText="Undo" onClick={() => console.log('Undo clicked')}>
            Undo
          </ToastAction>
          <ToastClose />
        </Toast>
      )}
    </>
  )
}

export const Default: Story = {
  render: () => <DefaultToastDemo />,
}

export const Destructive: Story = {
  render: () => <DestructiveToastDemo />,
}

export const WithAction: Story = {
  render: () => <WithActionToastDemo />,
}
