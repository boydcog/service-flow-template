import type { Meta, StoryObj } from '@storybook/react'
import { Input } from './input'

const meta = {
  title: 'Web/Input',
  component: Input,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    type: {
      control: 'select',
      options: ['text', 'email', 'password', 'number', 'date'],
    },
    disabled: {
      control: 'boolean',
    },
    error: {
      control: 'boolean',
    },
    placeholder: {
      control: 'text',
    },
  },
} satisfies Meta<typeof Input>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    placeholder: 'Enter text...',
    type: 'text',
  },
}

export const Email: Story = {
  args: {
    placeholder: 'Enter email...',
    type: 'email',
  },
}

export const Password: Story = {
  args: {
    placeholder: 'Enter password...',
    type: 'password',
  },
}

export const Number: Story = {
  args: {
    placeholder: 'Enter number...',
    type: 'number',
  },
}

export const Date: Story = {
  args: {
    type: 'date',
  },
}

export const Disabled: Story = {
  args: {
    placeholder: 'Disabled input',
    disabled: true,
  },
}

export const Error: Story = {
  args: {
    placeholder: 'Invalid input',
    error: true,
    value: 'Bad value',
  },
}
