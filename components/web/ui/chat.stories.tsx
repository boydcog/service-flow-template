import type { Meta, StoryObj } from "@storybook/react";
import { Chat, ChatBubble } from "./chat";
import type { ChatMessage } from "./chat";

// ─── Sample Data ──────────────────────────────────────────────────────────────

const now = new Date();
const minutesAgo = (n: number) => new Date(now.getTime() - n * 60 * 1000);

const sampleMessages: ChatMessage[] = [
  {
    id: "1",
    content: "안녕하세요! 오늘 미팅 일정 확인하고 싶어서요.",
    sender: "other",
    timestamp: minutesAgo(10),
  },
  {
    id: "2",
    content: "안녕하세요! 오후 2시에 예정되어 있습니다.",
    sender: "me",
    timestamp: minutesAgo(9),
    read: true,
  },
  {
    id: "3",
    content: "참석자 명단 파일 보내드릴게요.",
    sender: "me",
    timestamp: minutesAgo(8),
    read: true,
    attachments: [
      {
        id: "att-1",
        name: "참석자_명단.pdf",
        size: 204800,
        type: "file",
        url: "#",
      },
    ],
  },
  {
    id: "4",
    content: "감사합니다! 확인했어요.",
    sender: "other",
    timestamp: minutesAgo(5),
  },
  {
    id: "5",
    content: "혹시 회의실도 예약이 되어 있나요?",
    sender: "other",
    timestamp: minutesAgo(4),
  },
  {
    id: "6",
    content: "네, 3층 세미나실로 예약해두었습니다.",
    sender: "me",
    timestamp: minutesAgo(1),
    read: false,
  },
];

const fewMessages: ChatMessage[] = [
  {
    id: "a",
    content: "처음 보내는 메시지입니다.",
    sender: "other",
    timestamp: minutesAgo(2),
  },
  {
    id: "b",
    content: "반갑습니다!",
    sender: "me",
    timestamp: minutesAgo(1),
    read: true,
  },
];

const withImageMessages: ChatMessage[] = [
  {
    id: "img-1",
    content: "스크린샷 공유드립니다.",
    sender: "other",
    timestamp: minutesAgo(3),
    attachments: [
      {
        id: "att-img",
        name: "screenshot.png",
        size: 512000,
        type: "image",
        url: "https://via.placeholder.com/400x200",
      },
    ],
  },
  {
    id: "img-2",
    content: "잘 받았습니다. 확인할게요!",
    sender: "me",
    timestamp: minutesAgo(1),
    read: true,
  },
];

// ─── Meta ─────────────────────────────────────────────────────────────────────

const meta = {
  title: "Web/Chat",
  component: Chat,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    isTyping: {
      control: "boolean",
    },
    disabled: {
      control: "boolean",
    },
    typingUserName: {
      control: "text",
    },
    placeholder: {
      control: "text",
    },
  },
  decorators: [
    (Story: React.ComponentType) => (
      <div style={{ width: "420px", height: "560px" }}>
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Chat>;

export default meta;
type Story = StoryObj<typeof meta>;

// ─── Stories ──────────────────────────────────────────────────────────────────

/**
 * 기본 채팅 UI — 대화 목록 + 입력란
 */
export const Default: Story = {
  args: {
    messages: sampleMessages,
    isTyping: false,
  },
};

/**
 * 타이핑 인디케이터 표시
 */
export const TypingIndicator: Story = {
  args: {
    messages: fewMessages,
    isTyping: true,
    typingUserName: "김민지",
  },
};

/**
 * 이미지 첨부 메시지
 */
export const WithImageAttachment: Story = {
  args: {
    messages: withImageMessages,
    isTyping: false,
  },
};

/**
 * 비어있는 채팅방
 */
export const Empty: Story = {
  args: {
    messages: [],
    isTyping: false,
    placeholder: "첫 메시지를 보내보세요...",
  },
};

/**
 * 입력 비활성화 상태
 */
export const Disabled: Story = {
  args: {
    messages: fewMessages,
    disabled: true,
  },
};

/**
 * 단일 버블 컴포넌트 — 내 메시지 (읽음)
 */
export const BubbleMe: StoryObj<typeof ChatBubble> = {
  render: () => (
    <div style={{ width: "360px" }}>
      <ChatBubble
        message={{
          id: "b1",
          content: "안녕하세요, 잘 지내셨나요?",
          sender: "me",
          timestamp: new Date(),
          read: true,
        }}
      />
    </div>
  ),
};

/**
 * 단일 버블 컴포넌트 — 상대방 메시지
 */
export const BubbleOther: StoryObj<typeof ChatBubble> = {
  render: () => (
    <div style={{ width: "360px" }}>
      <ChatBubble
        message={{
          id: "b2",
          content: "네! 오랜만이에요.",
          sender: "other",
          timestamp: new Date(),
        }}
      />
    </div>
  ),
};
