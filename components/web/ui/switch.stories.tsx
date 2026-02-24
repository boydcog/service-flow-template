import type { Meta, StoryObj } from '@storybook/react'
import { useState } from 'react'
import { Switch } from './switch'

const meta = {
  title: 'Web/Switch',
  component: Switch,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof Switch>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => {
    const [checked, setChecked] = useState(false)
    return <Switch checked={checked} onCheckedChange={setChecked} />
  },
}

export const Checked: Story = {
  render: () => {
    const [checked, setChecked] = useState(true)
    return <Switch checked={checked} onCheckedChange={setChecked} />
  },
}

export const Disabled: Story = {
  render: () => <Switch disabled />,
}

export const DisabledChecked: Story = {
  render: () => <Switch disabled checked />,
}

export const WithLabel: Story = {
  render: () => {
    const [checked, setChecked] = useState(false)
    return (
      <div className="flex items-center space-x-2">
        <Switch id="airplane-mode" checked={checked} onCheckedChange={setChecked} />
        <label htmlFor="airplane-mode" className="text-sm font-medium">Airplane Mode</label>
      </div>
    )
  },
}

export const Multiple: Story = {
  render: () => {
    const [wifi, setWifi] = useState(true)
    const [bluetooth, setBlueooth] = useState(false)
    const [notifications, setNotifications] = useState(true)

    return (
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <Switch id="wifi" checked={wifi} onCheckedChange={setWifi} />
          <label htmlFor="wifi" className="text-sm font-medium">Wi-Fi</label>
        </div>
        <div className="flex items-center space-x-2">
          <Switch id="bluetooth" checked={bluetooth} onCheckedChange={setBlueooth} />
          <label htmlFor="bluetooth" className="text-sm font-medium">Bluetooth</label>
        </div>
        <div className="flex items-center space-x-2">
          <Switch id="notifications" checked={notifications} onCheckedChange={setNotifications} />
          <label htmlFor="notifications" className="text-sm font-medium">Notifications</label>
        </div>
      </div>
    )
  },
}
