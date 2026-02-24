import type { Meta, StoryObj } from '@storybook/react'
import { Skeleton } from './skeleton'

const meta = {
  title: 'Web/Skeleton',
  component: Skeleton,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof Skeleton>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    className: 'h-12 w-12',
  },
}

export const CircleAvatar: Story = {
  render: () => <Skeleton className="h-12 w-12 rounded-full" />,
}

export const Card: Story = {
  render: () => (
    <div className="rounded-lg border p-4 space-y-3">
      <Skeleton className="h-6 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
    </div>
  ),
}

export const PostCard: Story = {
  render: () => (
    <div className="space-y-4 p-4">
      <Skeleton className="h-[200px] w-full rounded-lg" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
      </div>
      <div className="flex gap-2">
        <Skeleton className="h-8 w-8 rounded-full" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-3 w-1/2" />
          <Skeleton className="h-3 w-1/3" />
        </div>
      </div>
    </div>
  ),
}

export const TableRow: Story = {
  render: () => (
    <div className="space-y-2">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <Skeleton className="h-8 w-8" />
          <Skeleton className="h-8 flex-1" />
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-8 w-24" />
        </div>
      ))}
    </div>
  ),
}
