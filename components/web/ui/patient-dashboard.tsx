import * as React from "react";
import { cn } from "@components/web/lib/utils";
import { Button } from "./button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./table";

/**
 * 컬럼 정의 타입
 */
export interface PatientColumn {
  key: string;
  label: string;
  render?: (value: unknown, row: Record<string, unknown>) => React.ReactNode;
  width?: string;
}

/**
 * 액션 버튼 정의 타입
 */
export interface PatientAction {
  label: string;
  onClick: (row: Record<string, unknown>) => void;
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon" | "icon-sm" | "icon-lg";
  icon?: React.ReactNode;
}

/**
 * 환자 대시보드 Props
 */
export interface PatientDashboardProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * 테이블 컬럼 정의 배열
   */
  columns: PatientColumn[];

  /**
   * 테이블 데이터 배열
   */
  data: Record<string, unknown>[];

  /**
   * 오른쪽 액션 버튼 배열 (선택사항)
   */
  actions?: PatientAction[];

  /**
   * 데이터 없을 때 표시할 메시지
   */
  emptyMessage?: string;

  /**
   * 로딩 상태
   */
  isLoading?: boolean;
}

/**
 * 환자 대시보드 컴포넌트
 *
 * 테이블 형태로 환자 정보를 관리하고, 동적 컬럼과 액션 버튼을 지원합니다.
 * 기존 Table, Button 컴포넌트를 조합하여 구성됩니다.
 *
 * @example
 * const columns: PatientColumn[] = [
 *   { key: 'name', label: '환자명' },
 *   { key: 'age', label: '나이' },
 *   { key: 'status', label: '상태', render: (value) => <Badge>{value}</Badge> },
 * ]
 *
 * const actions: PatientAction[] = [
 *   { label: '보기', onClick: (row) => console.log(row), size: 'sm' },
 *   { label: '수정', onClick: (row) => console.log(row), variant: 'outline', size: 'sm' },
 * ]
 *
 * <PatientDashboard
 *   columns={columns}
 *   data={patients}
 *   actions={actions}
 * />
 */
const PatientDashboard = React.forwardRef<HTMLDivElement, PatientDashboardProps>(
  (
    {
      columns,
      data,
      actions,
      emptyMessage = "데이터가 없습니다.",
      isLoading = false,
      className,
      ...props
    },
    ref,
  ) => {
    return (
      <div ref={ref} className={cn("w-full space-y-4", className)} {...props}>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                {columns.map((column) => (
                  <TableHead key={column.key} className={column.width}>
                    {column.label}
                  </TableHead>
                ))}
                {actions && actions.length > 0 && (
                  <TableHead className="text-right">작업</TableHead>
                )}
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell
                    colSpan={columns.length + (actions ? 1 : 0)}
                    className="text-center py-8 text-muted-foreground"
                  >
                    로딩 중...
                  </TableCell>
                </TableRow>
              ) : data.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={columns.length + (actions ? 1 : 0)}
                    className="text-center py-8 text-muted-foreground"
                  >
                    {emptyMessage}
                  </TableCell>
                </TableRow>
              ) : (
                data.map((row, rowIndex) => (
                  <TableRow key={rowIndex}>
                    {columns.map((column) => (
                      <TableCell key={`${rowIndex}-${column.key}`} className={column.width}>
                        {column.render
                          ? column.render(row[column.key], row)
                          : String(row[column.key] ?? "-")}
                      </TableCell>
                    ))}
                    {actions && actions.length > 0 && (
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          {actions.map((action, actionIndex) => (
                            <Button
                              key={actionIndex}
                              variant={action.variant ?? "default"}
                              size={action.size ?? "sm"}
                              onClick={() => action.onClick(row)}
                            >
                              {action.icon && <span>{action.icon}</span>}
                              {action.label}
                            </Button>
                          ))}
                        </div>
                      </TableCell>
                    )}
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    );
  },
);

PatientDashboard.displayName = "PatientDashboard";

export { PatientDashboard };
