import type { Meta, StoryObj } from '@storybook/react'
import { Header, HeaderContainer, HeaderLeft, HeaderRight, HeaderBrand } from './header'
import { Button } from './button'

const meta = {
  title: 'Web/Header',
  component: Header,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta<typeof Header>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Header>
      <HeaderContainer>
        <HeaderLeft>
          <HeaderBrand>MyApp</HeaderBrand>
        </HeaderLeft>
        <HeaderRight>
          <Button variant="ghost" size="sm">
            Profile
          </Button>
          <Button variant="outline" size="sm">
            Logout
          </Button>
        </HeaderRight>
      </HeaderContainer>
    </Header>
  ),
}

export const WithMenu: Story = {
  render: () => (
    <Header>
      <HeaderContainer>
        <HeaderLeft>
          <HeaderBrand>Logo</HeaderBrand>
          <nav className="hidden md:flex gap-4 text-sm">
            <a href="#" className="hover:text-primary">
              Home
            </a>
            <a href="#" className="hover:text-primary">
              About
            </a>
            <a href="#" className="hover:text-primary">
              Contact
            </a>
          </nav>
        </HeaderLeft>
        <HeaderRight>
          <Button variant="ghost" size="sm">
            Sign In
          </Button>
        </HeaderRight>
      </HeaderContainer>
    </Header>
  ),
}
