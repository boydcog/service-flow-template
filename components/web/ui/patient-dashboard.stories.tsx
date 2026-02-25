import type { Meta, StoryObj } from "@storybook/react";
import { PatientDashboard, type PatientColumn, type PatientAction } from "./patient-dashboard";

const meta = {
  title: "Web/PatientDashboard",
  component: PatientDashboard,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof PatientDashboard>;

export default meta;
type Story = StoryObj<typeof meta>;

// 샘플 데이터
const samplePatients = [
  {
    id: 1,
    name: "김환자",
    age: 45,
    phone: "010-1234-5678",
    status: "진료중",
    lastVisit: "2024-02-20",
  },
  {
    id: 2,
    name: "이대기",
    age: 62,
    phone: "010-2345-6789",
    status: "대기중",
    lastVisit: "2024-02-18",
  },
  {
    id: 3,
    name: "박완료",
    age: 38,
    phone: "010-3456-7890",
    status: "완료",
    lastVisit: "2024-02-15",
  },
  {
    id: 4,
    name: "최신규",
    age: 55,
    phone: "010-4567-8901",
    status: "진료중",
    lastVisit: "2024-02-21",
  },
];

const columns: PatientColumn[] = [
  { key: "name", label: "환자명" },
  { key: "age", label: "나이" },
  { key: "phone", label: "연락처" },
  { key: "status", label: "상태" },
  { key: "lastVisit", label: "마지막 방문" },
];

const actions: PatientAction[] = [
  {
    label: "보기",
    onClick: (row) => alert(`환자 보기: ${row.name}`),
    variant: "default",
    size: "sm",
  },
  {
    label: "수정",
    onClick: (row) => alert(`환자 수정: ${row.name}`),
    variant: "outline",
    size: "sm",
  },
  {
    label: "삭제",
    onClick: (row) => alert(`환자 삭제: ${row.name}`),
    variant: "destructive",
    size: "sm",
  },
];

/**
 * 기본 상태 - 기본 컬럼과 액션 버튼 포함
 */
export const Default: Story = {
  args: {
    columns,
    data: samplePatients,
    actions,
  },
};

/**
 * 액션 버튼 없음 - 테이블만 표시
 */
export const WithoutActions: Story = {
  args: {
    columns,
    data: samplePatients,
  },
};

/**
 * 커스텀 렌더링 - 상태에 따라 다른 색상 표시
 */
export const WithCustomRendering: Story = {
  args: {
    columns: [
      { key: "name", label: "환자명" },
      { key: "age", label: "나이" },
      { key: "phone", label: "연락처" },
      {
        key: "status",
        label: "상태",
        render: (value: unknown): React.ReactNode => {
          const statusColor: Record<string, string> = {
            진료중: "bg-blue-100 text-blue-800",
            대기중: "bg-yellow-100 text-yellow-800",
            완료: "bg-green-100 text-green-800",
          };
          const statusValue = String(value ?? "");
          return (
            <span
              className={`px-2 py-1 rounded text-xs font-medium ${statusColor[statusValue] || "bg-gray-100 text-gray-800"}`}
            >
              {statusValue}
            </span>
          );
        },
      },
      { key: "lastVisit", label: "마지막 방문" },
    ],
    data: samplePatients,
    actions: [
      {
        label: "상세보기",
        onClick: (row) => alert(`상세보기: ${row.name}`),
        variant: "default",
        size: "sm",
      },
    ],
  },
};

/**
 * 데이터 없음 - 빈 상태
 */
export const Empty: Story = {
  args: {
    columns,
    data: [],
    actions,
    emptyMessage: "등록된 환자가 없습니다.",
  },
};

/**
 * 로딩 상태
 */
export const Loading: Story = {
  args: {
    columns,
    data: [],
    actions,
    isLoading: true,
  },
};

/**
 * 간단한 액션 - 조회, 수정만
 */
export const SimpleActions: Story = {
  args: {
    columns,
    data: samplePatients,
    actions: [
      {
        label: "조회",
        onClick: (row) => alert(`조회: ${row.name}`),
        size: "sm",
      },
      {
        label: "수정",
        onClick: (row) => alert(`수정: ${row.name}`),
        variant: "outline",
        size: "sm",
      },
    ],
  },
};

/**
 * 단일 액션 - 보기만
 */
export const SingleAction: Story = {
  args: {
    columns,
    data: samplePatients,
    actions: [
      {
        label: "상세정보",
        onClick: (row) => alert(`상세정보: ${row.name}`),
      },
    ],
  },
};

/**
 * 최소 컬럼 - 필수 정보만
 */
export const MinimalColumns: Story = {
  args: {
    columns: [
      { key: "name", label: "이름" },
      { key: "phone", label: "전화" },
    ],
    data: samplePatients,
    actions: [
      {
        label: "보기",
        onClick: (row) => alert(`${row.name} 보기`),
        size: "sm",
      },
    ],
  },
};
