import type { Meta, StoryObj } from '@storybook/react'
import { Navbar, NavbarItem, NavbarMenu, NavbarItemGroup } from './navbar'

const meta = {
  title: 'Web/Navbar',
  component: Navbar,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta<typeof Navbar>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Navbar>
      <NavbarItem href="#" data-active>
        Home
      </NavbarItem>
      <NavbarItem href="#">About</NavbarItem>
      <NavbarItem href="#">Services</NavbarItem>
      <NavbarItem href="#">Contact</NavbarItem>
      <NavbarMenu>
        <NavbarItemGroup>
          <NavbarItem href="#">Sign In</NavbarItem>
        </NavbarItemGroup>
      </NavbarMenu>
    </Navbar>
  ),
}

export const WithGroups: Story = {
  render: () => (
    <Navbar>
      <NavbarItemGroup>
        <NavbarItem href="#" data-active>
          Dashboard
        </NavbarItem>
        <NavbarItem href="#">Reports</NavbarItem>
      </NavbarItemGroup>
      <NavbarMenu>
        <NavbarItemGroup>
          <NavbarItem href="#">Settings</NavbarItem>
          <NavbarItem href="#">Logout</NavbarItem>
        </NavbarItemGroup>
      </NavbarMenu>
    </Navbar>
  ),
}
