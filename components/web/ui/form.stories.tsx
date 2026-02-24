/* @ts-nocheck - story files allow flexible types */
import type { Meta, StoryObj } from '@storybook/react'
import { useForm } from 'react-hook-form'
import { Form, FormItem, FormControl, FormMessage, FormField, FormLabel } from './form'
import { Input } from './input'
import { Button } from './button'
import { Checkbox } from './checkbox'

const meta = {
  title: 'Web/Form',
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

function DefaultFormContent() {
  const form = useForm({
    defaultValues: {
      email: '',
      subscribe: false,
    },
  })

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(() => console.log('submitted'))}
        className="w-96 space-y-4"
      >
        {/* @ts-expect-error - strict type checking for story flexibility */}
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="Enter your email" type="email" {...(field as Record<string, unknown>)} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* @ts-expect-error - strict type checking for story flexibility */}
        <FormField
          control={form.control}
          name="subscribe"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Checkbox label="Subscribe to newsletter" checked={field.value as boolean} onCheckedChange={field.onChange} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}

function ComplexFormContent() {
  const form = useForm({
    defaultValues: {
      firstName: '',
      lastName: '',
      email: '',
      terms: false,
    },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(() => console.log('submitted'))} className="w-96 space-y-4">
        <FormField
          control={form.control}
          name="firstName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>First Name</FormLabel>
              <FormControl>
                <Input placeholder="John" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="lastName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Last Name</FormLabel>
              <FormControl>
                <Input placeholder="Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="john@example.com" type="email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="terms"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Checkbox label="Accept terms and conditions" checked={field.value} onCheckedChange={field.onChange} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" className="w-full">
          Register
        </Button>
      </form>
    </Form>
  )
}

export const Default: Story = {
  render: () => <DefaultFormContent />,
}

export const WithValidationError: Story = {
  render: () => {
    function FormWithError() {
      const form = useForm({
        defaultValues: {
          email: '',
        },
      })

      return (
        <Form {...form}>
          <form className="w-96 space-y-4">
            <FormField
              control={form.control}
              name="email"
              rules={{
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email',
                },
              }}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter your email" type="email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit">Submit</Button>
          </form>
        </Form>
      )
    }
    return <FormWithError />
  },
}

export const ComplexForm: Story = {
  render: () => <ComplexFormContent />,
}
