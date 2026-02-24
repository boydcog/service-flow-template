import type { Meta, StoryObj } from '@storybook/react'
import { useState } from 'react'
import { RadioGroup, RadioGroupItem } from './radio'

const meta = {
  title: 'Web/Radio',
  component: RadioGroup,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof RadioGroup>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState('option-1')
    return (
      <RadioGroup value={value} onValueChange={setValue}>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="option-1" id="option-1" />
          <label className="text-sm font-medium" htmlFor="option-1">Option 1</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="option-2" id="option-2" />
          <label className="text-sm font-medium" htmlFor="option-2">Option 2</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="option-3" id="option-3" />
          <label className="text-sm font-medium" htmlFor="option-3">Option 3</label>
        </div>
      </RadioGroup>
    )
  },
}

export const Disabled: Story = {
  render: () => (
    <RadioGroup defaultValue="option-1">
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="option-1" id="option-1" />
        <label className="text-sm font-medium" htmlFor="option-1">Option 1</label>
      </div>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="option-2" id="option-2" disabled />
        <label className="text-sm font-medium" htmlFor="option-2">Option 2 (Disabled)</label>
      </div>
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="option-3" id="option-3" />
        <label className="text-sm font-medium" htmlFor="option-3">Option 3</label>
      </div>
    </RadioGroup>
  ),
}

export const Vertical: Story = {
  render: () => {
    const [value, setValue] = useState('email')
    return (
      <RadioGroup value={value} onValueChange={setValue} className="space-y-3">
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="email" id="email" />
          <label className="text-sm font-medium" htmlFor="email">Email notifications</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="sms" id="sms" />
          <label className="text-sm font-medium" htmlFor="sms">SMS notifications</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="push" id="push" />
          <label className="text-sm font-medium" htmlFor="push">Push notifications</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="none" id="none" />
          <label className="text-sm font-medium" htmlFor="none">No notifications</label>
        </div>
      </RadioGroup>
    )
  },
}
