import type { Meta, StoryObj } from '@storybook/react'
import { StatCard } from './stat-card'
import { TrendingUp, Users, ShoppingCart, DollarSign } from 'lucide-react'

const meta = {
  title: 'Web/StatCard',
  component: StatCard,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof StatCard>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    label: 'Total Revenue',
    value: '$45,231.89',
    change: { value: 20.1, direction: 'up' },
  },
}

export const WithIcon: Story = {
  args: {
    label: 'Total Visitors',
    value: '12,450',
    change: { value: 12.5, direction: 'up' },
    icon: <Users className="h-6 w-6 text-primary" />,
  },
}

export const Decline: Story = {
  args: {
    label: 'Sales',
    value: '2,543',
    change: { value: 5.2, direction: 'down' },
    icon: <ShoppingCart className="h-6 w-6 text-destructive" />,
  },
}

export const NoChange: Story = {
  args: {
    label: 'Active Users',
    value: '8,234',
    icon: <Users className="h-6 w-6 text-secondary" />,
  },
}

export const Grid: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4">
      <StatCard
        label="Total Revenue"
        value="$45,231.89"
        change={{ value: 20.1, direction: 'up' }}
        icon={<DollarSign className="h-6 w-6 text-primary" />}
      />
      <StatCard
        label="Total Visitors"
        value="12,450"
        change={{ value: 12.5, direction: 'up' }}
        icon={<Users className="h-6 w-6 text-blue-500" />}
      />
      <StatCard
        label="Sales"
        value="2,543"
        change={{ value: 5.2, direction: 'down' }}
        icon={<ShoppingCart className="h-6 w-6 text-orange-500" />}
      />
      <StatCard
        label="Growth"
        value="23%"
        change={{ value: 8.1, direction: 'up' }}
        icon={<TrendingUp className="h-6 w-6 text-green-500" />}
      />
    </div>
  ),
}
