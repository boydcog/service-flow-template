import type { Meta, StoryObj } from '@storybook/react'
import { Popover, PopoverTrigger, PopoverContent } from './popover'
import { Button } from './button'

const meta = {
  title: 'Web/Popover',
  component: Popover,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof Popover>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Open Popover</Button>
      </PopoverTrigger>
      <PopoverContent>
        <div className="space-y-2">
          <h4 className="font-medium leading-none">Popover Title</h4>
          <p className="text-sm text-muted-foreground">
            This is a popover content. You can put any content here.
          </p>
        </div>
      </PopoverContent>
    </Popover>
  ),
}

export const WithForm: Story = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Open Settings</Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="space-y-4">
          <div className="space-y-2">
            <h4 className="font-medium leading-none">Settings</h4>
            <p className="text-sm text-muted-foreground">
              Configure your preferences here
            </p>
          </div>
          <div className="space-y-2">
            <label htmlFor="width" className="text-sm font-medium">
              Width
            </label>
            <input
              id="width"
              defaultValue="100%"
              className="w-full px-3 py-2 border border-input rounded-md text-sm"
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="max-width" className="text-sm font-medium">
              Max. width
            </label>
            <input
              id="max-width"
              defaultValue="300px"
              className="w-full px-3 py-2 border border-input rounded-md text-sm"
            />
          </div>
        </div>
      </PopoverContent>
    </Popover>
  ),
}

export const Sides: Story = {
  render: () => (
    <div className="flex gap-4">
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Top</Button>
        </PopoverTrigger>
        <PopoverContent side="top">
          This popover appears on top
        </PopoverContent>
      </Popover>

      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Right</Button>
        </PopoverTrigger>
        <PopoverContent side="right">
          This popover appears on the right
        </PopoverContent>
      </Popover>

      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Bottom</Button>
        </PopoverTrigger>
        <PopoverContent side="bottom">
          This popover appears at the bottom
        </PopoverContent>
      </Popover>

      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline">Left</Button>
        </PopoverTrigger>
        <PopoverContent side="left">
          This popover appears on the left
        </PopoverContent>
      </Popover>
    </div>
  ),
}
