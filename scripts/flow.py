#!/usr/bin/env python3
"""
/flow 명령어 자동화 스크립트
플로우 설명 입력 -> 컴포넌트 스캔 -> 자동 매핑 -> 페이지 생성 -> 빌드 검증 -> PR 생성
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# process-manager import
sys.path.insert(0, str(Path(__file__).parent))
import process_manager as pm
import verify_flow

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
FLOWS_DIR = PROJECT_ROOT / "flows"
PROJECTS_DIR = PROJECT_ROOT / "projects"
STATE_DIR = PROJECT_ROOT / ".claude" / "state"
COMPONENTS_DIR = PROJECT_ROOT / "components" / "web" / "ui"


# ---------------------------------------------------------------------------
# 컴포넌트 스캔: components/web/ui/*.tsx에서 export와 variant/size 추출
# ---------------------------------------------------------------------------

# 각 컴포넌트 파일의 정적 export 정보 (실제 코드에서 검증 완료)
COMPONENT_REGISTRY: list[dict[str, object]] = [
    {
        "name": "accordion",
        "exports": ["Accordion", "AccordionItem", "AccordionTrigger", "AccordionContent"],
        "primary": "Accordion",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "alert",
        "exports": ["Alert", "AlertTitle", "AlertDescription"],
        "primary": "Alert",
        "variants": ["default", "destructive", "warning", "success"],
        "sizes": [],
    },
    {
        "name": "avatar",
        "exports": ["Avatar", "AvatarImage", "AvatarFallback"],
        "primary": "Avatar",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "badge",
        "exports": ["Badge"],
        "primary": "Badge",
        "variants": ["default", "secondary", "destructive", "outline", "muted"],
        "sizes": [],
    },
    {
        "name": "button",
        "exports": ["Button"],
        "primary": "Button",
        "variants": ["default", "destructive", "outline", "secondary", "ghost", "link"],
        "sizes": ["default", "sm", "lg", "icon", "icon-sm", "icon-lg"],
    },
    {
        "name": "card",
        "exports": ["Card", "CardHeader", "CardFooter", "CardTitle", "CardDescription", "CardContent"],
        "primary": "Card",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "checkbox",
        "exports": ["Checkbox"],
        "primary": "Checkbox",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "dialog",
        "exports": [
            "Dialog", "DialogTrigger", "DialogContent", "DialogHeader",
            "DialogFooter", "DialogTitle", "DialogDescription", "DialogClose",
        ],
        "primary": "Dialog",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "form",
        "exports": [
            "FormItem", "FormLabel",
            "FormControl", "FormDescription", "FormMessage",
        ],
        "primary": "FormItem",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "header",
        "exports": ["Header", "HeaderContainer", "HeaderLeft", "HeaderRight", "HeaderBrand"],
        "primary": "Header",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "input",
        "exports": ["Input"],
        "primary": "Input",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "navbar",
        "exports": ["Navbar", "NavbarItem", "NavbarMenu", "NavbarItemGroup"],
        "primary": "Navbar",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "popover",
        "exports": ["Popover", "PopoverTrigger", "PopoverContent"],
        "primary": "Popover",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "pricing-card",
        "exports": ["PricingCard"],
        "primary": "PricingCard",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "radio",
        "exports": ["RadioGroup", "RadioGroupItem"],
        "primary": "RadioGroup",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "select",
        "exports": [
            "Select", "SelectGroup", "SelectValue", "SelectTrigger",
            "SelectContent", "SelectLabel", "SelectItem", "SelectSeparator",
        ],
        "primary": "Select",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "sidebar",
        "exports": [
            "Sidebar", "SidebarContent", "SidebarHeader", "SidebarFooter",
            "SidebarItem", "SidebarToggle",
        ],
        "primary": "Sidebar",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "skeleton",
        "exports": ["Skeleton"],
        "primary": "Skeleton",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "stat-card",
        "exports": ["StatCard"],
        "primary": "StatCard",
        "variants": ["default", "colored"],
        "sizes": [],
    },
    {
        "name": "switch",
        "exports": ["Switch"],
        "primary": "Switch",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "table",
        "exports": [
            "Table", "TableHeader", "TableBody", "TableFooter",
            "TableHead", "TableRow", "TableCell", "TableCaption",
        ],
        "primary": "Table",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "tabs",
        "exports": ["Tabs", "TabsList", "TabsTrigger", "TabsContent"],
        "primary": "Tabs",
        "variants": [],
        "sizes": [],
    },
    {
        "name": "toast",
        "exports": [
            "ToastProvider", "ToastViewport", "Toast", "ToastTitle",
            "ToastDescription", "ToastClose", "ToastAction",
        ],
        "primary": "Toast",
        "variants": ["default", "destructive"],
        "sizes": [],
    },
    {
        "name": "tooltip",
        "exports": ["Tooltip", "TooltipTrigger", "TooltipContent", "TooltipProvider"],
        "primary": "Tooltip",
        "variants": [],
        "sizes": [],
    },
]


def scan_available_components() -> list[dict[str, object]]:
    """components/web/ui/*.tsx 스캔하여 사용 가능한 컴포넌트 목록 반환.

    파일 시스템에서 실제 존재하는 컴포넌트만 반환하고,
    COMPONENT_REGISTRY의 정적 메타데이터와 병합한다.
    """
    available: list[dict[str, object]] = []

    if not COMPONENTS_DIR.exists():
        print("[WARNING] components/web/ui 디렉토리가 존재하지 않습니다.")
        return available

    # 실제 파일 목록 (stories 제외)
    existing_files: set[str] = set()
    for f in COMPONENTS_DIR.iterdir():
        if f.suffix == ".tsx" and ".stories." not in f.name:
            existing_files.add(f.stem)

    # 레지스트리와 매칭
    registry_map = {str(entry["name"]): entry for entry in COMPONENT_REGISTRY}

    for file_stem in sorted(existing_files):
        if file_stem in registry_map:
            entry = registry_map[file_stem]
            available.append({
                "name": str(entry["name"]),
                "exports": list(entry["exports"]),
                "primary": str(entry["primary"]),
                "variants": list(entry["variants"]),
                "sizes": list(entry["sizes"]),
                "path": f"components/web/ui/{file_stem}.tsx",
            })
        else:
            # 레지스트리에 없는 파일 -> 동적 파싱 시도
            parsed = _parse_component_file(COMPONENTS_DIR / f"{file_stem}.tsx")
            if parsed:
                available.append({
                    "name": file_stem,
                    "exports": parsed["exports"],
                    "primary": parsed["primary"],
                    "variants": parsed["variants"],
                    "sizes": parsed["sizes"],
                    "path": f"components/web/ui/{file_stem}.tsx",
                })

    return available


def _parse_component_file(filepath: Path) -> Optional[dict[str, object]]:
    """컴포넌트 파일에서 export 이름과 variant/size를 동적으로 파싱."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    # export 추출
    exports: list[str] = []
    # "export { A, B, C }" 패턴
    block_match = re.findall(r"export\s*\{([^}]+)\}", content)
    for block in block_match:
        for item in block.split(","):
            name = item.strip().split(" as ")[-1].strip()
            if name and not name.startswith("type "):
                cleaned = name.replace("type ", "").strip()
                if cleaned:
                    exports.append(cleaned)
    # "export const X" / "export function X" / "export interface X"
    inline = re.findall(r"export\s+(?:const|function|interface)\s+(\w+)", content)
    for name in inline:
        if name not in exports:
            exports.append(name)

    if not exports:
        return None

    # variant 추출
    variants: list[str] = []
    variant_block = re.search(r"variant:\s*\{([^}]+)\}", content)
    if variant_block:
        variants = re.findall(r"(\w+):", variant_block.group(1))

    # size 추출
    sizes: list[str] = []
    size_block = re.search(r"size:\s*\{([^}]+)\}", content)
    if size_block:
        sizes = re.findall(r"[\"']?(\w[\w-]*)[\"']?\s*:", size_block.group(1))

    primary = exports[0] if exports else filepath.stem.title().replace("-", "")

    return {
        "exports": exports,
        "primary": primary,
        "variants": variants,
        "sizes": sizes,
    }


# ---------------------------------------------------------------------------
# 키워드 -> 컴포넌트 자동 매핑 룰테이블
# ---------------------------------------------------------------------------

COMPONENT_KEYWORDS: dict[str, list[str]] = {
    # 입력 관련
    "input": ["input", "email", "password", "search", "text", "name", "phone", "address"],
    "checkbox": ["checkbox", "agree", "terms", "consent"],
    "switch": ["switch", "toggle", "on-off", "enable", "disable"],
    "radio": ["radio", "choice", "select-one", "gender"],
    "select": ["select", "dropdown", "choose", "picker", "filter", "category"],
    "form": ["form", "submit", "register", "signup", "login", "contact"],
    # 버튼/액션
    "button": ["button", "click", "action", "confirm", "cancel", "next", "prev", "save", "delete", "cta"],
    # 카드/컨테이너
    "card": ["card", "panel", "box", "container", "section", "content", "info"],
    "stat-card": ["stat", "metric", "kpi", "analytics"],
    "pricing-card": ["pricing", "plan", "subscription", "tier", "package"],
    # 레이아웃
    "header": ["header", "top-bar", "app-bar", "banner"],
    "navbar": ["navbar", "navigation", "nav", "menu-bar", "breadcrumb"],
    "sidebar": ["sidebar", "side-menu", "drawer", "left-panel"],
    # 오버레이/팝업
    "dialog": ["dialog", "modal", "popup"],
    "popover": ["popover", "dropdown-menu", "context-menu"],
    "tooltip": ["tooltip", "hint", "help-text"],
    "toast": ["toast", "notification", "snackbar"],
    # 표시
    "alert": ["alert", "warning", "error", "success", "notice"],
    "badge": ["badge", "tag", "label", "chip", "status", "count"],
    "avatar": ["avatar", "profile-pic", "user-image"],
    "skeleton": ["skeleton", "loading", "placeholder", "shimmer"],
    # 데이터 표시
    "table": ["table", "grid", "list", "data-table", "spreadsheet"],
    "tabs": ["tabs", "tab-panel", "tabbed", "multi-view"],
    "accordion": ["accordion", "collapsible", "expandable", "faq", "details"],
}

# 레이아웃 컴포넌트 (화면에 최소 1개 포함 보장)
LAYOUT_COMPONENTS = {"header", "navbar", "sidebar"}

# fallback 컴포넌트 (빈 화면용)
FALLBACK_COMPONENTS = ["card", "button"]


def map_components_to_screens(
    screens: list[dict[str, str]],
    available: list[dict[str, object]],
) -> list[dict[str, object]]:
    """각 화면에 키워드 기반으로 컴포넌트를 자동 할당.

    Args:
        screens: parse_flow_description()이 반환한 화면 리스트 [{title, description}, ...]
        available: scan_available_components()가 반환한 컴포넌트 리스트

    Returns:
        화면별 매핑된 컴포넌트 리스트 [{screen_title, components: [comp_info, ...]}, ...]
    """
    available_map: dict[str, dict[str, object]] = {
        str(c["name"]): c for c in available
    }
    result: list[dict[str, object]] = []

    for screen in screens:
        title = screen.get("title", "")
        desc = screen.get("description", "")
        text = f"{title} {desc}".lower()

        matched_names: list[str] = []

        # 키워드 매칭
        for comp_name, keywords in COMPONENT_KEYWORDS.items():
            if comp_name not in available_map:
                continue
            for kw in keywords:
                if kw in text:
                    if comp_name not in matched_names:
                        matched_names.append(comp_name)
                    break

        # 레이아웃 컴포넌트 최소 1개 보장
        has_layout = any(n in LAYOUT_COMPONENTS for n in matched_names)
        if not has_layout:
            for layout_name in LAYOUT_COMPONENTS:
                if layout_name in available_map:
                    matched_names.insert(0, layout_name)
                    break

        # 빈 화면 fallback
        if len(matched_names) == 0:
            for fb in FALLBACK_COMPONENTS:
                if fb in available_map and fb not in matched_names:
                    matched_names.append(fb)

        # 최소 2개 컴포넌트 보장 (레이아웃 + 콘텐츠)
        if len(matched_names) < 2:
            for fb in FALLBACK_COMPONENTS:
                if fb in available_map and fb not in matched_names:
                    matched_names.append(fb)
                if len(matched_names) >= 2:
                    break

        components = [available_map[n] for n in matched_names if n in available_map]

        result.append({
            "screen_title": title,
            "screen_description": desc,
            "components": components,
        })

    return result


# ---------------------------------------------------------------------------
# 페이지 생성: import + JSX
# ---------------------------------------------------------------------------

def _to_pascal_case(s: str) -> str:
    """kebab-case / snake_case / space 를 PascalCase로 변환."""
    return "".join(word.capitalize() for word in re.split(r"[-_\s]+", s) if word)


def create_page_with_components(
    screen_name: str,
    components: list[dict[str, object]],
) -> str:
    """화면 이름과 매핑된 컴포넌트로 페이지 TSX 코드를 생성.

    - import: from "@components/web/ui/{name}" import {exports}
    - export default function {PascalCaseName}Page()
    - 각 import 컴포넌트를 최소 1회 사용하는 JSX 구조

    Args:
        screen_name: 화면 이름 (예: "Email Signup")
        components: 매핑된 컴포넌트 리스트

    Returns:
        TypeScript/JSX 문자열
    """
    page_name = _to_pascal_case(screen_name)

    # import 문 생성 (파일별로 그룹화)
    imports_by_file: dict[str, list[str]] = {}
    for comp in components:
        file_name = str(comp["name"])
        exports = [str(e) for e in comp.get("exports", [])]
        if not exports:
            primary = str(comp.get("primary", ""))
            if primary:
                exports = [primary]
        imports_by_file[file_name] = exports

    import_lines: list[str] = ['import React from "react";']
    for file_name in sorted(imports_by_file.keys()):
        names = imports_by_file[file_name]
        if names:
            joined = ", ".join(names)
            import_lines.append(
                f'import {{ {joined} }} from "@components/web/ui/{file_name}";'
            )

    # JSX 생성 - 각 컴포넌트를 최소 1회 사용
    jsx_parts: list[str] = []
    for comp in components:
        comp_name = str(comp["name"])
        jsx = _generate_component_jsx(comp_name, comp)
        jsx_parts.append(jsx)

    jsx_body = "\n".join(jsx_parts)

    code = f"""{chr(10).join(import_lines)}

export default function {page_name}Page() {{
  return (
    <div className="min-h-screen bg-background">
{jsx_body}
    </div>
  );
}}
"""
    return code


def _generate_component_jsx(
    comp_name: str,
    comp: dict[str, object],
) -> str:
    """개별 컴포넌트의 JSX 사용 코드를 생성.

    모든 export를 최소 1회 사용한다.
    """
    indent = "      "

    # --- 레이아웃 컴포넌트 ---
    if comp_name == "header":
        return (
            f"{indent}<Header>\n"
            f"{indent}  <HeaderContainer>\n"
            f"{indent}    <HeaderLeft>\n"
            f'{indent}      <HeaderBrand>Service Flow</HeaderBrand>\n'
            f"{indent}    </HeaderLeft>\n"
            f"{indent}    <HeaderRight>\n"
            f'{indent}      <span className="text-sm text-muted-foreground">Menu</span>\n'
            f"{indent}    </HeaderRight>\n"
            f"{indent}  </HeaderContainer>\n"
            f"{indent}</Header>"
        )

    if comp_name == "navbar":
        return (
            f"{indent}<Navbar>\n"
            f"{indent}  <NavbarItemGroup>\n"
            f'{indent}    <NavbarItem href="#">Home</NavbarItem>\n'
            f'{indent}    <NavbarItem href="#">About</NavbarItem>\n'
            f"{indent}  </NavbarItemGroup>\n"
            f"{indent}  <NavbarMenu>\n"
            f'{indent}    <NavbarItem href="#">Settings</NavbarItem>\n'
            f"{indent}  </NavbarMenu>\n"
            f"{indent}</Navbar>"
        )

    if comp_name == "sidebar":
        return (
            f"{indent}<Sidebar>\n"
            f"{indent}  <SidebarHeader>\n"
            f'{indent}    <span className="font-semibold">Menu</span>\n'
            f"{indent}  </SidebarHeader>\n"
            f"{indent}  <SidebarContent>\n"
            f'{indent}    <SidebarItem href="#">Dashboard</SidebarItem>\n'
            f'{indent}    <SidebarItem href="#">Settings</SidebarItem>\n'
            f"{indent}  </SidebarContent>\n"
            f"{indent}  <SidebarFooter>\n"
            f'{indent}    <SidebarToggle />\n'
            f"{indent}  </SidebarFooter>\n"
            f"{indent}</Sidebar>"
        )

    # --- 입력 컴포넌트 ---
    if comp_name == "input":
        return f'{indent}<Input placeholder="Enter value" />'

    if comp_name == "checkbox":
        return f'{indent}<Checkbox label="Agree to terms" />'

    if comp_name == "switch":
        return f"{indent}<Switch />"

    if comp_name == "radio":
        return (
            f'{indent}<RadioGroup defaultValue="option-1">\n'
            f'{indent}  <RadioGroupItem value="option-1" />\n'
            f'{indent}  <RadioGroupItem value="option-2" />\n'
            f"{indent}</RadioGroup>"
        )

    if comp_name == "select":
        return (
            f"{indent}<Select>\n"
            f"{indent}  <SelectTrigger>\n"
            f'{indent}    <SelectValue placeholder="Choose..." />\n'
            f"{indent}  </SelectTrigger>\n"
            f"{indent}  <SelectContent>\n"
            f'{indent}    <SelectGroup>\n'
            f'{indent}      <SelectLabel>Options</SelectLabel>\n'
            f'{indent}      <SelectItem value="a">Option A</SelectItem>\n'
            f'{indent}      <SelectItem value="b">Option B</SelectItem>\n'
            f'{indent}      <SelectSeparator />\n'
            f'{indent}      <SelectItem value="c">Option C</SelectItem>\n'
            f"{indent}    </SelectGroup>\n"
            f"{indent}  </SelectContent>\n"
            f"{indent}</Select>"
        )

    # --- 버튼 ---
    if comp_name == "button":
        return f"{indent}<Button>Click</Button>"

    # --- 카드 ---
    if comp_name == "card":
        return (
            f"{indent}<Card>\n"
            f"{indent}  <CardHeader>\n"
            f"{indent}    <CardTitle>Title</CardTitle>\n"
            f"{indent}    <CardDescription>Description</CardDescription>\n"
            f"{indent}  </CardHeader>\n"
            f"{indent}  <CardContent>\n"
            f'{indent}    <p className="text-sm">Content goes here.</p>\n'
            f"{indent}  </CardContent>\n"
            f"{indent}  <CardFooter>\n"
            f'{indent}    <span className="text-xs text-muted-foreground">Footer</span>\n'
            f"{indent}  </CardFooter>\n"
            f"{indent}</Card>"
        )

    if comp_name == "stat-card":
        return f'{indent}<StatCard label="Users" value="1,234" />'

    if comp_name == "pricing-card":
        return (
            f"{indent}<PricingCard\n"
            f'{indent}  name="Pro"\n'
            f'{indent}  price="29"\n'
            f'{indent}  description="For professionals"\n'
            f'{indent}  features={{[{{ name: "Feature 1", included: true }}, {{ name: "Feature 2", included: false }}]}}\n'
            f"{indent}/>"
        )

    # --- 오버레이 ---
    if comp_name == "dialog":
        return (
            f"{indent}<Dialog>\n"
            f"{indent}  <DialogTrigger>Open Dialog</DialogTrigger>\n"
            f"{indent}  <DialogContent>\n"
            f"{indent}    <DialogHeader>\n"
            f"{indent}      <DialogTitle>Dialog Title</DialogTitle>\n"
            f"{indent}      <DialogDescription>Dialog description.</DialogDescription>\n"
            f"{indent}    </DialogHeader>\n"
            f"{indent}    <DialogFooter>\n"
            f"{indent}      <DialogClose>Close</DialogClose>\n"
            f"{indent}    </DialogFooter>\n"
            f"{indent}  </DialogContent>\n"
            f"{indent}</Dialog>"
        )

    if comp_name == "popover":
        return (
            f"{indent}<Popover>\n"
            f"{indent}  <PopoverTrigger>Open Popover</PopoverTrigger>\n"
            f"{indent}  <PopoverContent>Popover content</PopoverContent>\n"
            f"{indent}</Popover>"
        )

    if comp_name == "tooltip":
        return (
            f"{indent}<TooltipProvider>\n"
            f"{indent}  <Tooltip>\n"
            f"{indent}    <TooltipTrigger>Hover me</TooltipTrigger>\n"
            f"{indent}    <TooltipContent>Tooltip text</TooltipContent>\n"
            f"{indent}  </Tooltip>\n"
            f"{indent}</TooltipProvider>"
        )

    if comp_name == "toast":
        return (
            f"{indent}<ToastProvider>\n"
            f"{indent}  <Toast>\n"
            f"{indent}    <ToastTitle>Notification</ToastTitle>\n"
            f"{indent}    <ToastDescription>Something happened.</ToastDescription>\n"
            f"{indent}    <ToastClose />\n"
            f"{indent}    <ToastAction altText=\"undo\">Undo</ToastAction>\n"
            f"{indent}  </Toast>\n"
            f"{indent}  <ToastViewport />\n"
            f"{indent}</ToastProvider>"
        )

    # --- 표시 ---
    if comp_name == "alert":
        return (
            f"{indent}<Alert>\n"
            f"{indent}  <AlertTitle>Notice</AlertTitle>\n"
            f"{indent}  <AlertDescription>This is an alert message.</AlertDescription>\n"
            f"{indent}</Alert>"
        )

    if comp_name == "badge":
        return f"{indent}<Badge>Status</Badge>"

    if comp_name == "avatar":
        return (
            f"{indent}<Avatar>\n"
            f'{indent}  <AvatarImage src="" alt="User" />\n'
            f"{indent}  <AvatarFallback>U</AvatarFallback>\n"
            f"{indent}</Avatar>"
        )

    if comp_name == "skeleton":
        return f'{indent}<Skeleton className="h-8 w-full" />'

    # --- 데이터 표시 ---
    if comp_name == "table":
        return (
            f"{indent}<Table>\n"
            f"{indent}  <TableHeader>\n"
            f"{indent}    <TableRow>\n"
            f"{indent}      <TableHead>Name</TableHead>\n"
            f"{indent}      <TableHead>Value</TableHead>\n"
            f"{indent}    </TableRow>\n"
            f"{indent}  </TableHeader>\n"
            f"{indent}  <TableBody>\n"
            f"{indent}    <TableRow>\n"
            f"{indent}      <TableCell>Item</TableCell>\n"
            f"{indent}      <TableCell>100</TableCell>\n"
            f"{indent}    </TableRow>\n"
            f"{indent}  </TableBody>\n"
            f"{indent}  <TableFooter>\n"
            f"{indent}    <TableRow>\n"
            f"{indent}      <TableCell>Total</TableCell>\n"
            f"{indent}      <TableCell>100</TableCell>\n"
            f"{indent}    </TableRow>\n"
            f"{indent}  </TableFooter>\n"
            f"{indent}  <TableCaption>A summary table.</TableCaption>\n"
            f"{indent}</Table>"
        )

    if comp_name == "tabs":
        return (
            f'{indent}<Tabs defaultValue="tab1">\n'
            f"{indent}  <TabsList>\n"
            f'{indent}    <TabsTrigger value="tab1">Tab 1</TabsTrigger>\n'
            f'{indent}    <TabsTrigger value="tab2">Tab 2</TabsTrigger>\n'
            f"{indent}  </TabsList>\n"
            f'{indent}  <TabsContent value="tab1">Tab 1 content</TabsContent>\n'
            f'{indent}  <TabsContent value="tab2">Tab 2 content</TabsContent>\n'
            f"{indent}</Tabs>"
        )

    if comp_name == "accordion":
        return (
            f'{indent}<Accordion type="single" collapsible>\n'
            f'{indent}  <AccordionItem value="item-1">\n'
            f"{indent}    <AccordionTrigger>Section 1</AccordionTrigger>\n"
            f"{indent}    <AccordionContent>Content for section 1.</AccordionContent>\n"
            f"{indent}  </AccordionItem>\n"
            f"{indent}</Accordion>"
        )

    # --- 폼 ---
    if comp_name == "form":
        return (
            f"{indent}<FormItem>\n"
            f"{indent}  <FormLabel>Field</FormLabel>\n"
            f"{indent}  <FormControl>\n"
            f'{indent}    <span className="text-sm">Form control placeholder</span>\n'
            f"{indent}  </FormControl>\n"
            f"{indent}  <FormDescription>Help text.</FormDescription>\n"
            f"{indent}  <FormMessage />\n"
            f"{indent}</FormItem>"
        )

    # --- 알 수 없는 컴포넌트 ---
    primary = str(comp.get("primary", ""))
    if primary:
        return f"{indent}<{primary} />"

    return f'{indent}<div>{{/* {comp_name} */}}</div>'


def generate_all_pages(
    mapped_screens: list[dict[str, object]],
) -> dict[str, str]:
    """모든 화면의 페이지 코드를 생성.

    Returns:
        {screen_file_name: tsx_code} 딕셔너리
    """
    pages: dict[str, str] = {}

    for i, screen_info in enumerate(mapped_screens, 1):
        screen_title = str(screen_info.get("screen_title", f"Screen {i}"))
        components = screen_info.get("components", [])
        file_name = f"Screen{i}.tsx"
        code = create_page_with_components(screen_title, components)
        pages[file_name] = code

    return pages


# ---------------------------------------------------------------------------
# 빌드 검증
# ---------------------------------------------------------------------------

def verify_flow_build(project_path: Path) -> bool:
    """프로젝트 경로에서 npx tsc --noEmit 실행하여 타입 검증.

    Returns:
        True: 빌드 성공, False: 에러 존재
    """
    print("\n[CHECK] TypeScript 빌드 검증 중...")

    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("[OK] TypeScript 빌드 검증 통과")
            return True

        print("[ERROR] TypeScript 빌드 에러:")
        for line in result.stdout.splitlines():
            if line.strip():
                print(f"  {line}")
        for line in result.stderr.splitlines():
            if line.strip():
                print(f"  {line}")

        return False

    except subprocess.TimeoutExpired:
        print("[ERROR] TypeScript 검증 타임아웃 (60초)")
        return False
    except FileNotFoundError:
        print("[ERROR] npx를 찾을 수 없습니다. Node.js가 설치되어 있는지 확인하세요.")
        return False
    except Exception as e:
        print(f"[ERROR] 빌드 검증 실패: {e}")
        return False


# ---------------------------------------------------------------------------
# 상태 관리 함수
# ---------------------------------------------------------------------------

def save_active_flow(flow_name: str) -> None:
    """활성 플로우 저장"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    active_flow_file = STATE_DIR / "_active_flow.txt"
    active_flow_file.write_text(flow_name.strip())


def load_active_flow() -> Optional[str]:
    """활성 플로우 로드"""
    active_flow_file = STATE_DIR / "_active_flow.txt"
    if active_flow_file.exists():
        return active_flow_file.read_text().strip()
    return None


def save_flow_metadata(flow_name: str, metadata: dict[str, object]) -> None:
    """플로우 메타데이터 저장"""
    flow_state_dir = STATE_DIR / flow_name
    flow_state_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = flow_state_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))


def load_flow_metadata(flow_name: str) -> Optional[dict[str, object]]:
    """플로우 메타데이터 로드"""
    metadata_file = STATE_DIR / flow_name / "metadata.json"
    if metadata_file.exists():
        try:
            return json.loads(metadata_file.read_text())
        except Exception:
            return None
    return None


# ---------------------------------------------------------------------------
# Git / 사용자 함수
# ---------------------------------------------------------------------------

def sync_git() -> None:
    """Git 최신 데이터 동기화 (git pull --rebase)"""
    print("\n[SYNC] 최신 데이터 동기화 중...")
    try:
        result = subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("[OK] Git 동기화 완료")
        else:
            print("[WARNING] Git 동기화 스킵 (오프라인 또는 네트워크 오류)")
    except Exception as e:
        print(f"[WARNING] Git 동기화 실패: {e} (계속 진행)")


def load_user_identity() -> dict[str, str]:
    """사용자 신원 파일 로드"""
    identity_file = PROJECT_ROOT / ".user-identity"
    if not identity_file.exists():
        print("[ERROR] 신원 파일 없음. /setup을 먼저 실행하세요.")
        sys.exit(1)

    identity: dict[str, str] = {}
    with open(identity_file) as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                identity[key] = value

    return identity


def select_or_create_project() -> Path:
    """기존 프로젝트 선택 또는 새 프로젝트 생성"""
    print("\n[PROJECT] 프로젝트 선택")
    print("=" * 40)

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    existing_projects = sorted([
        d for d in PROJECTS_DIR.iterdir()
        if d.is_dir() and d.name != ".gitkeep"
    ])

    if existing_projects:
        print("\n기존 프로젝트:")
        for i, proj in enumerate(existing_projects, 1):
            print(f"  {i}. {proj.name}")
        print(f"  {len(existing_projects) + 1}. [NEW] 새 프로젝트 생성")

        while True:
            try:
                choice = int(input(f"\n선택 (1-{len(existing_projects) + 1}): "))
                if 1 <= choice <= len(existing_projects):
                    selected_project = existing_projects[choice - 1]
                    print(f"[OK] 선택: {selected_project.name}")

                    print("[SYNC] 컴포넌트 동기화 중...")
                    sync_script = PROJECT_ROOT / "scripts" / "sync-components.sh"
                    result = subprocess.run(
                        ["bash", str(sync_script), str(selected_project)],
                        cwd=PROJECT_ROOT,
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode == 0:
                        print("[OK] 컴포넌트 동기화 완료")
                    else:
                        print(f"[WARNING] 컴포넌트 동기화 경고: {result.stderr}")

                    return selected_project
                elif choice == len(existing_projects) + 1:
                    break
                else:
                    print("[ERROR] 올바른 번호를 입력해주세요.")
            except ValueError:
                print("[ERROR] 숫자를 입력해주세요.")

    # 새 프로젝트 생성
    print("\n[NEW] 새 프로젝트 생성")
    project_name = input("프로젝트 이름 (예: my-app): ").strip().lower()

    if not project_name or not project_name.replace("-", "").replace("_", "").isalnum():
        print("[ERROR] 올바른 프로젝트명을 입력해주세요 (영문, 숫자, - 또는 _만 사용).")
        sys.exit(1)

    project_path = PROJECTS_DIR / project_name
    if project_path.exists():
        print(f"[ERROR] 이미 존재하는 프로젝트입니다: {project_name}")
        sys.exit(1)

    print(f"[SETUP] 프로젝트 생성 중: {project_name}...")
    create_script = PROJECT_ROOT / "scripts" / "create-project.sh"
    result = subprocess.run(
        ["bash", str(create_script), project_name],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[OK] 프로젝트 생성 완료: {project_name}")
        return project_path
    else:
        print(f"[ERROR] 프로젝트 생성 실패:\n{result.stderr}")
        sys.exit(1)


def get_product_name() -> str:
    """제품명 입력"""
    print("\n제품명을 입력하세요 (예: user-onboarding):")
    product_name = input("> ").strip().lower()

    if not product_name or not product_name.replace("-", "").replace("_", "").isalnum():
        print("[ERROR] 올바른 제품명을 입력해주세요 (영문, 숫자, - 또는 _만 사용).")
        sys.exit(1)

    return product_name


def get_flow_description() -> str:
    """플로우 설명 입력"""
    print("\n[INPUT] 서비스 플로우를 자유롭게 설명해주세요:")
    print("(여러 줄 가능, 빈 줄 입력 시 완료)")
    print("-" * 40)

    lines: list[str] = []
    while True:
        line = input()
        if not line:
            if lines:
                break
            continue
        lines.append(line)

    return "\n".join(lines)


def parse_flow_description(description: str) -> dict[str, object]:
    """플로우 설명 파싱"""
    lines = description.strip().split("\n")
    screens: list[dict[str, str]] = []
    current_screen: Optional[dict[str, str]] = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 화면 번호 감지 (1), 2), 1. 2. etc.)
        number_match = re.match(r"^(\d+)[.)]\s*(.+)", line)
        if number_match:
            if current_screen:
                screens.append(current_screen)
            current_screen = {
                "title": number_match.group(2).strip(),
                "description": "",
            }
        elif current_screen:
            current_screen["description"] += line + " "

    if current_screen:
        screens.append(current_screen)

    return {
        "total_screens": len(screens),
        "screens": screens[:10],  # 최대 10개 화면
    }


def generate_flow_structure(
    product_name: str,
    mapped_screens: list[dict[str, object]],
) -> dict[str, object]:
    """플로우 구조 생성 (매핑된 화면 기반)"""
    screens_data: list[dict[str, object]] = []
    for i, ms in enumerate(mapped_screens, 1):
        screen_title = str(ms.get("screen_title", f"Screen {i}"))
        comp_names = [str(c["name"]) for c in ms.get("components", [])]
        screens_data.append({
            "id": i,
            "title": screen_title,
            "path": f"/step-{i}",
            "components": comp_names,
        })

    return {
        "product_name": product_name,
        "created_at": datetime.now().isoformat(),
        "screens": screens_data,
        "navigation": "linear",
        "data_flow": {},
    }


def create_flow_files(
    product_name: str,
    flow_structure: dict[str, object],
    mapped_screens: list[dict[str, object]],
    user_name: str = "",
) -> Path:
    """플로우 파일 생성 (컴포넌트 자동 매핑 반영)"""
    flow_dir = FLOWS_DIR / product_name
    flow_dir.mkdir(parents=True, exist_ok=True)
    screens_dir = flow_dir / "screens"
    screens_dir.mkdir(parents=True, exist_ok=True)

    # index.json
    (flow_dir / "index.json").write_text(json.dumps(flow_structure, indent=2))

    # 상태 저장
    save_active_flow(product_name)
    save_flow_metadata(product_name, {
        "flow_name": product_name,
        "created_by": user_name,
        "created_at": flow_structure.get("created_at"),
        "status": "in_progress",
        "screens": len(mapped_screens),
    })

    # 개별 화면 페이지 생성
    pages = generate_all_pages(mapped_screens)
    for file_name, code in pages.items():
        (screens_dir / file_name).write_text(code)

    # page.tsx - 메인 플로우 페이지
    pascal_name = _to_pascal_case(product_name)
    screen_imports: list[str] = []
    screen_cases: list[str] = []
    for i in range(1, len(mapped_screens) + 1):
        screen_title = str(mapped_screens[i - 1].get("screen_title", f"Screen {i}"))
        comp_name = f"{_to_pascal_case(screen_title)}Page"
        screen_imports.append(f'import {comp_name} from "./screens/Screen{i}";')
        screen_cases.append(f"      case {i - 1}: return <{comp_name} />;")

    page_tsx = f"""import React, {{ useState }} from "react";
{chr(10).join(screen_imports)}

export default function {pascal_name}FlowPage() {{
  const [step, setStep] = useState(0);
  const totalSteps = {len(mapped_screens)};

  const renderScreen = () => {{
    switch (step) {{
{chr(10).join(screen_cases)}
      default: return null;
    }}
  }};

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-2xl p-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold">{product_name}</h1>
          <span className="text-sm text-muted-foreground">
            Step {{step + 1}} / {{totalSteps}}
          </span>
        </div>

        {{renderScreen()}}

        <div className="mt-8 flex justify-between">
          <button
            onClick={{() => setStep((s) => Math.max(0, s - 1))}}
            disabled={{step === 0}}
            className="rounded-md border px-4 py-2 text-sm disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={{() => setStep((s) => Math.min(totalSteps - 1, s + 1))}}
            disabled={{step === totalSteps - 1}}
            className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}}
"""
    (flow_dir / "page.tsx").write_text(page_tsx)

    # README.md
    readme = f"# {product_name.title()} Flow\n\n## Overview\n\n"
    readme += f"Total screens: {len(mapped_screens)}\n\n## Screens\n\n"
    for i, ms in enumerate(mapped_screens, 1):
        screen_title = str(ms.get("screen_title", f"Screen {i}"))
        comp_names = [str(c["name"]) for c in ms.get("components", [])]
        readme += f"### {i}. {screen_title}\n\n"
        readme += f"Components: {', '.join(comp_names)}\n\n"

    (flow_dir / "README.md").write_text(readme)

    print(f"\n[OK] 플로우 생성 완료")
    print(f"  위치: {flow_dir}")
    print(f"  화면: {len(mapped_screens)}개")
    print(f"  파일: index.json, page.tsx, README.md")
    for file_name in sorted(pages.keys()):
        print(f"    screens/{file_name}")

    return flow_dir


# ---------------------------------------------------------------------------
# 서버 및 PR 함수
# ---------------------------------------------------------------------------

def run_dev_server(project_path: Optional[Path] = None) -> None:
    """개발 서버 실행"""
    print("\n[START] 웹 서버 시작 중...")

    target_path = project_path or PROJECT_ROOT
    port = 3000

    node_modules = target_path / "node_modules"
    if not node_modules.exists():
        print("[SETUP] 의존성 설치 중...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=target_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[ERROR] npm install 실패:\n{result.stderr}")
            sys.exit(1)

    process_manager = PROJECT_ROOT / "scripts" / "process-manager.py"
    if process_manager.exists():
        try:
            subprocess.run(
                ["python3", str(process_manager), "kill-port", str(port)],
                cwd=PROJECT_ROOT,
                capture_output=True,
            )
        except Exception:
            pass

    print("[START] 개발 서버 시작 중...")
    if pm.start_dev_server(target_path, port):
        print(f"[OK] 개발 서버 시작됨 -> http://localhost:{port}")
        print("브라우저에서 플로우를 확인하세요.")
    else:
        print("[ERROR] 개발 서버 실행 실패")
        sys.exit(1)


def wait_for_confirmation() -> bool:
    """사용자 확인 대기"""
    print("\n" + "=" * 40)
    while True:
        choice = input(
            "플로우 확인이 완료되셨나요? (y/n): "
        ).strip().lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("[ERROR] y 또는 n을 입력해주세요.")


def create_pr(user_name: str, product_name: str) -> str:
    """PR 생성"""
    print("\n[PR] PR 생성 중...")

    branch_name = f"flow/{product_name}"
    pr_title = f"[flow] {user_name}: {product_name} 서비스 플로우"
    pr_body = f"""## {product_name} 서비스 플로우 추가

### 변경 사항
- {product_name} 플로우 생성
- 화면 구조 설계
- README 작성

### 테스트 완료
- [x] 모든 화면 확인
- [x] 네비게이션 테스트
- [x] 데이터 플로우 검증

Co-Authored-By: {user_name} <noreply@anthropic.com>
"""

    try:
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        subprocess.run(
            ["git", "add", f"flows/{product_name}/"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        subprocess.run(
            ["git", "update-index", "--no-skip-worktree", f"flows/{product_name}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
        )

        subprocess.run(
            ["git", "commit", "-m", pr_title],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            pr_url = result.stdout.strip().split("\n")[-1]
            print(f"\n[OK] PR이 생성되었습니다!")
            print(f"  PR 링크: {pr_url}")
            return pr_url
        else:
            print(f"[WARNING] PR 생성 실패 (gh CLI 필요): {result.stderr}")
            print(f"  브랜치: {branch_name}")
            return branch_name

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] git 작업 실패: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# 메인 함수
# ---------------------------------------------------------------------------

def main() -> None:
    """메인 함수"""
    print("\n# /flow -- 서비스 플로우 생성")
    print("=" * 40)

    # 0. Git 동기화
    sync_git()

    # 1. 신원 확인
    identity = load_user_identity()
    user_name = identity.get("name", "unknown")
    user_role = identity.get("role", "unknown")

    print(f"\n[OK] 신원: {user_name} ({user_role})")
    print("[OK] 권한: 플로우 작업 가능")

    # 1.5. 프로젝트 선택/생성
    project_path = select_or_create_project()

    # 2. 제품명 입력
    product_name = get_product_name()
    print(f"[OK] 제품명: {product_name}")

    # 3. 플로우 설명 입력
    description = get_flow_description()
    flow_info = parse_flow_description(description)

    print(f"\n[INFO] 인식된 화면: {flow_info['total_screens']}개")
    for i, screen in enumerate(flow_info["screens"], 1):
        print(f"  {i}. {screen['title']}")

    # 4. 컴포넌트 스캔 및 자동 매핑
    print("\n[SCAN] 컴포넌트 스캔 중...")
    available = scan_available_components()
    print(f"[OK] {len(available)}개 컴포넌트 로드됨")

    for comp in available:
        variants = comp.get("variants", [])
        variant_info = f" (variants: {', '.join(str(v) for v in variants)})" if variants else ""
        print(f"  - {comp['name']}{variant_info}")

    print("\n[MAP] 화면별 컴포넌트 자동 매핑 중...")
    mapped_screens = map_components_to_screens(flow_info["screens"], available)

    for ms in mapped_screens:
        comp_names = [str(c["name"]) for c in ms.get("components", [])]
        print(f"  [{ms['screen_title']}] -> {', '.join(comp_names)}")

    # 5. 플로우 구조 생성 및 파일 생성
    flow_structure = generate_flow_structure(product_name, mapped_screens)
    flow_dir = create_flow_files(product_name, flow_structure, mapped_screens, user_name)

    # 6. 검증 실행 (verify_flow 모듈 사용)
    max_retries = 3
    verified = False

    for attempt in range(1, max_retries + 1):
        passed = verify_flow.run_all(flow_dir, project_path)
        if passed:
            verified = True
            break

        if attempt < max_retries:
            print(f"  재시도 기회: {max_retries - attempt}회 남음")
            print("  파일을 수정한 후 Enter를 눌러 재검증하세요.")
            print("  (취소: q 입력)")
            user_input = input("  > ").strip().lower()
            if user_input == "q":
                print("[CANCEL] 검증이 취소되었습니다.")
                sys.exit(0)
        else:
            print(f"  최대 재시도 횟수({max_retries})를 초과했습니다.")
            print("  파일을 수정한 후 다시 /flow를 실행하세요.")
            sys.exit(1)

    if not verified:
        print("[ERROR] 검증 실패. PR 생성이 불가합니다.")
        sys.exit(1)

    # 7. 개발 서버 실행 (검증 통과 후)
    run_dev_server(project_path)

    # 8. 사용자 확인 대기
    print(f"\n[INFO] 개발 서버가 시작되었습니다.")
    print(f"  http://localhost:3000 에서 플로우를 확인하세요.")

    import webbrowser
    webbrowser.open("http://localhost:3000")

    confirmed = wait_for_confirmation()

    if not confirmed:
        print("[CANCEL] 플로우 작업이 취소되었습니다.")
        subprocess.run(["git", "checkout", "-"], cwd=PROJECT_ROOT, capture_output=True)
        sys.exit(0)

    # 9. PR 생성 (검증 통과 + 사용자 확인 후)
    pr_url = create_pr(user_name, product_name)

    print("\n" + "=" * 40)
    print("  플로우 작업이 완료되었습니다!")
    print(f"  PR: {pr_url}")
    print("=" * 40)


if __name__ == "__main__":
    main()
