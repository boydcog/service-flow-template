import type { Meta, StoryObj } from '@storybook/react'
import { PricingCard } from './pricing-card'

const meta = {
  title: 'Web/PricingCard',
  component: PricingCard,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof PricingCard>

export default meta
type Story = StoryObj<typeof meta>

const basicFeatures = [
  { name: 'Up to 10 projects', included: true },
  { name: '5GB storage', included: true },
  { name: 'Basic support', included: true },
  { name: 'Advanced analytics', included: false },
  { name: 'Priority support', included: false },
]

const proFeatures = [
  { name: 'Unlimited projects', included: true },
  { name: '100GB storage', included: true },
  { name: 'Priority support', included: true },
  { name: 'Advanced analytics', included: true },
  { name: 'Custom integrations', included: false },
]

const businessFeatures = [
  { name: 'Unlimited projects', included: true },
  { name: 'Unlimited storage', included: true },
  { name: '24/7 support', included: true },
  { name: 'Advanced analytics', included: true },
  { name: 'Custom integrations', included: true },
]

export const Default: Story = {
  args: {
    name: 'Plus',
    price: '29',
    description: 'For growing teams',
    features: proFeatures,
    cta: 'Start free trial',
  },
}

export const Featured: Story = {
  args: {
    name: 'Pro',
    price: '79',
    description: 'Most popular',
    features: proFeatures,
    cta: 'Start free trial',
    featured: true,
    badge: 'POPULAR',
  },
}

export const Comparison: Story = {
  render: () => (
    <div className="grid grid-cols-3 gap-6">
      <PricingCard
        name="Starter"
        price="19"
        description="For individuals"
        features={basicFeatures}
        cta="Get Started"
      />
      <PricingCard
        name="Pro"
        price="79"
        description="Most popular"
        features={proFeatures}
        cta="Start free trial"
        featured={true}
        badge="POPULAR"
      />
      <PricingCard
        name="Enterprise"
        price="199"
        description="For large teams"
        features={businessFeatures}
        cta="Contact Sales"
      />
    </div>
  ),
}
