import type { Meta, StoryObj } from '@storybook/react'
import { Sidebar, SidebarContent, SidebarHeader, SidebarFooter, SidebarItem } from './sidebar'

const meta = {
  title: 'Web/Sidebar',
  component: Sidebar,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta<typeof Sidebar>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Sidebar>
      <SidebarHeader>
        <h2 className="font-semibold">Menu</h2>
      </SidebarHeader>
      <SidebarContent className="space-y-1">
        <SidebarItem href="#" data-active>
          Dashboard
        </SidebarItem>
        <SidebarItem href="#">Projects</SidebarItem>
        <SidebarItem href="#">Tasks</SidebarItem>
        <SidebarItem href="#">Reports</SidebarItem>
      </SidebarContent>
      <SidebarFooter>
        <SidebarItem href="#">Settings</SidebarItem>
      </SidebarFooter>
    </Sidebar>
  ),
}

export const WithSections: Story = {
  render: () => (
    <Sidebar>
      <SidebarHeader>
        <h2 className="font-semibold">App</h2>
      </SidebarHeader>
      <SidebarContent className="space-y-4">
        <div>
          <div className="text-xs font-semibold text-muted-foreground px-4 py-2">Main</div>
          <SidebarItem href="#" data-active>
            Dashboard
          </SidebarItem>
          <SidebarItem href="#">Overview</SidebarItem>
        </div>
        <div>
          <div className="text-xs font-semibold text-muted-foreground px-4 py-2">Management</div>
          <SidebarItem href="#">Users</SidebarItem>
          <SidebarItem href="#">Roles</SidebarItem>
        </div>
      </SidebarContent>
      <SidebarFooter>
        <SidebarItem href="#">Logout</SidebarItem>
      </SidebarFooter>
    </Sidebar>
  ),
}
