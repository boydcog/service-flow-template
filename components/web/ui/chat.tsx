import * as React from "react";
import { cn } from "@components/web/lib/utils";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface ChatMessage {
  id: string;
  content: string;
  sender: "me" | "other";
  timestamp: Date;
  read?: boolean;
  attachments?: ChatAttachment[];
}

export interface ChatAttachment {
  id: string;
  name: string;
  size: number;
  type: "image" | "file";
  url: string;
}

export interface ChatProps extends React.HTMLAttributes<HTMLDivElement> {
  messages: ChatMessage[];
  currentUserId?: string;
  isTyping?: boolean;
  typingUserName?: string;
  onSendMessage?: (content: string, attachments: File[]) => void;
  placeholder?: string;
  disabled?: boolean;
}

export interface ChatBubbleProps extends React.HTMLAttributes<HTMLDivElement> {
  message: ChatMessage;
  showTime?: boolean;
}

export interface ChatInputProps extends React.HTMLAttributes<HTMLDivElement> {
  onSend?: (content: string, attachments: File[]) => void;
  placeholder?: string;
  disabled?: boolean;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatTime(date: Date): string {
  return date.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ─── ReadIcon ─────────────────────────────────────────────────────────────────

function ReadIcon({ read }: { read: boolean }) {
  return (
    <span
      className={cn(
        "inline-flex items-center text-xs",
        read ? "text-[var(--primary)]" : "text-[var(--muted-foreground)]"
      )}
      aria-label={read ? "읽음" : "전송됨"}
    >
      <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">
        <path
          d="M1 5L4.5 8.5L10 2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {read && (
          <path
            d="M5 5L8.5 8.5L14 2"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}
      </svg>
    </span>
  );
}

// ─── TypingIndicator ──────────────────────────────────────────────────────────

function TypingIndicator({ userName }: { userName?: string }) {
  return (
    <div className="flex items-end gap-2 px-4 py-1" aria-live="polite" aria-label="상대방 입력 중">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[var(--muted)] text-xs font-medium text-[var(--muted-foreground)]">
        {userName ? userName[0].toUpperCase() : "?"}
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-bl-sm bg-[var(--muted)] px-3 py-2">
        <span className="sr-only">{userName ?? "상대방"}이 입력 중입니다</span>
        <span
          className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted-foreground)]"
          style={{ animationDelay: "0ms" }}
          aria-hidden="true"
        />
        <span
          className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted-foreground)]"
          style={{ animationDelay: "150ms" }}
          aria-hidden="true"
        />
        <span
          className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted-foreground)]"
          style={{ animationDelay: "300ms" }}
          aria-hidden="true"
        />
      </div>
    </div>
  );
}

// ─── AttachmentPreview ────────────────────────────────────────────────────────

function AttachmentPreview({ attachment }: { attachment: ChatAttachment }) {
  if (attachment.type === "image") {
    return (
      <a
        href={attachment.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block overflow-hidden rounded-lg border border-[var(--border)]"
        aria-label={`이미지: ${attachment.name}`}
      >
        <img
          src={attachment.url}
          alt={attachment.name}
          className="max-h-48 w-full object-cover"
        />
      </a>
    );
  }

  return (
    <a
      href={attachment.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-2 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm transition-colors hover:bg-[var(--muted)]"
      aria-label={`파일 다운로드: ${attachment.name}`}
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        aria-hidden="true"
        className="shrink-0 text-[var(--muted-foreground)]"
      >
        <path
          d="M4 2h6l4 4v8a1 1 0 01-1 1H3a1 1 0 01-1-1V3a1 1 0 011-1z"
          stroke="currentColor"
          strokeWidth="1.2"
        />
        <path d="M9 2v4h4" stroke="currentColor" strokeWidth="1.2" />
      </svg>
      <div className="min-w-0 flex-1">
        <p className="truncate font-medium text-[var(--foreground)]">{attachment.name}</p>
        <p className="text-xs text-[var(--muted-foreground)]">{formatFileSize(attachment.size)}</p>
      </div>
    </a>
  );
}

// ─── ChatBubble ───────────────────────────────────────────────────────────────

const ChatBubble = React.forwardRef<HTMLDivElement, ChatBubbleProps>(
  ({ message, showTime = true, className, ...props }, ref) => {
    const isMe = message.sender === "me";

    return (
      <div
        ref={ref}
        className={cn("flex w-full items-end gap-2 px-4 py-1", isMe ? "flex-row-reverse" : "flex-row", className)}
        {...props}
      >
        {!isMe && (
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[var(--secondary)] text-xs font-medium text-[var(--secondary-foreground)]">
            O
          </div>
        )}

        <div className={cn("flex max-w-[70%] flex-col gap-1", isMe ? "items-end" : "items-start")}>
          {message.attachments && message.attachments.length > 0 && (
            <div className="flex w-full flex-col gap-1.5">
              {message.attachments.map((att) => (
                <AttachmentPreview key={att.id} attachment={att} />
              ))}
            </div>
          )}

          {message.content && (
            <div
              className={cn(
                "rounded-2xl px-3 py-2 text-sm leading-relaxed",
                isMe
                  ? "rounded-br-sm bg-[var(--primary)] text-[var(--primary-foreground)]"
                  : "rounded-bl-sm bg-[var(--muted)] text-[var(--foreground)]"
              )}
            >
              {message.content}
            </div>
          )}

          {showTime && (
            <div className={cn("flex items-center gap-1", isMe ? "flex-row-reverse" : "flex-row")}>
              <time
                className="text-xs text-[var(--muted-foreground)]"
                dateTime={message.timestamp.toISOString()}
              >
                {formatTime(message.timestamp)}
              </time>
              {isMe && message.read !== undefined && <ReadIcon read={message.read} />}
            </div>
          )}
        </div>
      </div>
    );
  }
);
ChatBubble.displayName = "ChatBubble";

// ─── ChatInput ────────────────────────────────────────────────────────────────

const ChatInput = React.forwardRef<HTMLDivElement, ChatInputProps>(
  ({ onSend, placeholder = "메시지를 입력하세요...", disabled = false, className, ...props }, ref) => {
    const [text, setText] = React.useState("");
    const [pendingFiles, setPendingFiles] = React.useState<File[]>([]);
    const fileInputRef = React.useRef<HTMLInputElement>(null);
    const textareaRef = React.useRef<HTMLTextAreaElement>(null);

    const handleSend = React.useCallback(() => {
      const trimmed = text.trim();
      if (!trimmed && pendingFiles.length === 0) return;
      onSend?.(trimmed, pendingFiles);
      setText("");
      setPendingFiles([]);
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }, [text, pendingFiles, onSend]);

    const handleKeyDown = React.useCallback(
      (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      },
      [handleSend]
    );

    const handleTextChange = React.useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
      setText(e.target.value);
      const el = e.target;
      el.style.height = "auto";
      el.style.height = `${Math.min(el.scrollHeight, 120)}px`;
    }, []);

    const handleFileChange = React.useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
      const files = Array.from(e.target.files ?? []);
      if (files.length === 0) return;
      setPendingFiles((prev) => [...prev, ...files]);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }, []);

    const removeFile = React.useCallback((index: number) => {
      setPendingFiles((prev) => prev.filter((_, i) => i !== index));
    }, []);

    const canSend = text.trim().length > 0 || pendingFiles.length > 0;

    return (
      <div
        ref={ref}
        className={cn("border-t border-[var(--border)] bg-[var(--background)] p-3", className)}
        {...props}
      >
        {pendingFiles.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {pendingFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center gap-1.5 rounded-md border border-[var(--border)] bg-[var(--muted)] px-2 py-1 text-xs"
              >
                <span className="max-w-32 truncate text-[var(--foreground)]">{file.name}</span>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                  aria-label={`${file.name} 첨부 제거`}
                >
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                    <path
                      d="M2 2l8 8M10 2l-8 8"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="flex items-end gap-2">
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="sr-only"
            onChange={handleFileChange}
            disabled={disabled}
            aria-label="파일 첨부"
            tabIndex={-1}
          />

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md text-[var(--muted-foreground)] transition-colors hover:bg-[var(--muted)] hover:text-[var(--foreground)] disabled:pointer-events-none disabled:opacity-50"
            aria-label="파일 첨부"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
              <path
                d="M15.5 8.5L8 16a4.243 4.243 0 01-6-6L9.5 2.5a2.828 2.828 0 014 4L7 13a1.414 1.414 0 01-2-2l6.5-6.5"
                stroke="currentColor"
                strokeWidth="1.4"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

          <textarea
            ref={textareaRef}
            value={text}
            onChange={handleTextChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="flex-1 resize-none rounded-md border border-[var(--border)] bg-[var(--input)] px-3 py-2 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--ring)] disabled:pointer-events-none disabled:opacity-50"
            style={{ minHeight: "44px", maxHeight: "160px" }}
            aria-label="메시지 입력"
          />

          <button
            type="button"
            onClick={handleSend}
            disabled={disabled || !canSend}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] transition-colors hover:bg-[var(--primary)]/90 disabled:pointer-events-none disabled:opacity-50"
            aria-label="메시지 전송"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path
                d="M14 8L2 2l2 6-2 6 12-6z"
                stroke="currentColor"
                strokeWidth="1.4"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>

      </div>
    );
  }
);
ChatInput.displayName = "ChatInput";

// ─── Chat ─────────────────────────────────────────────────────────────────────

/**
 * 전체 채팅 UI 컴포넌트.
 * 메시지 목록, 타이핑 인디케이터, 입력란을 포함합니다.
 *
 * @param props - ChatProps
 * @returns 렌더링된 채팅 UI
 */
const Chat = React.forwardRef<HTMLDivElement, ChatProps>(
  (
    {
      messages,
      isTyping = false,
      typingUserName,
      onSendMessage,
      placeholder,
      disabled = false,
      className,
      ...props
    },
    ref
  ) => {
    const scrollRef = React.useRef<HTMLDivElement>(null);

    React.useEffect(() => {
      if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
      }
    }, [messages, isTyping]);

    return (
      <div
        ref={ref}
        className={cn(
          "flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--background)]",
          className
        )}
        {...props}
      >
        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto py-3"
          role="log"
          aria-live="polite"
          aria-label="채팅 메시지 목록"
        >
          {messages.length === 0 && (
            <div className="flex h-full items-center justify-center py-8 text-sm text-[var(--muted-foreground)]">
              아직 메시지가 없습니다.
            </div>
          )}

          {messages.map((message) => (
            <ChatBubble key={message.id} message={message} />
          ))}

          {isTyping && <TypingIndicator userName={typingUserName} />}
        </div>

        <ChatInput onSend={onSendMessage} placeholder={placeholder} disabled={disabled} />
      </div>
    );
  }
);
Chat.displayName = "Chat";

export { Chat, ChatBubble, ChatInput };
