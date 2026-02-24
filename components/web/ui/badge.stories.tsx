import type { Meta, StoryObj } from '@storybook/react'
import { Badge } from './badge'

const meta = {
  title: 'Web/Badge',
  component: Badge,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'destructive', 'outline', 'muted'],
    },
  },
} satisfies Meta<typeof Badge>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: 'Badge',
    variant: 'default',
  },
}

export const Secondary: Story = {
  args: {
    children: 'Secondary',
    variant: 'secondary',
  },
}

export const Destructive: Story = {
  args: {
    children: 'Destructive',
    variant: 'destructive',
  },
}

export const Outline: Story = {
  args: {
    children: 'Outline',
    variant: 'outline',
  },
}

export const Muted: Story = {
  args: {
    children: 'Muted',
    variant: 'muted',
  },
}

export const Multiple: Story = {
  render: () => (
    <div className="flex gap-2">
      <Badge>Feature</Badge>
      <Badge variant="secondary">New</Badge>
      <Badge variant="destructive">Alert</Badge>
      <Badge variant="outline">Info</Badge>
      <Badge variant="muted">Disabled</Badge>
    </div>
  ),
}
