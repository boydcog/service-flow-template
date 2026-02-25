# Role-Based Workflows — Service Flow Template

**컴포넌트 라이브러리 개발을 위한 역할별 자동화 워크플로우**

---

## Overview

각 역할별로 **자동 검증 + 환경 실행**을 통합한 워크플로우입니다.

| 역할 | 명령어 | 검증 과정 | 실행 환경 | 사용 사례 |
|------|--------|---------|---------|---------|
| **Designer** | `npm run designer` | Lint → Type → Test | Storybook (6006) | 컴포넌트 개발 |
| **PM** | `npm run pm` | Lint → Type → Test | Dev Server (3001) | 서비스 플로우 |
| **Admin** | `npm run admin` | Lint → Type → Test | 메뉴 + 선택 | 템플릿 관리 |

---

## Designer Workflow

**컴포넌트 개발 및 시각화**

### Command
```bash
npm run designer
```

### Execution Flow
```
1 Lint Check
 ├─ ESLint validation
 ├─ Code style check
 └─ Pass → Continue

2 Type Check
 ├─ TypeScript compilation
 ├─ Type safety validation
 └─ Warnings allowed → Continue

3 Test Suite
 ├─ Component tests
 ├─ Unit tests
 └─ Pass → Continue

4 Storybook Launch
 ├─ http://localhost:6006/
 ├─ Hot reload enabled
 └─ Interactive component stories
```

### Features
- Automatic code validation
- Hot module reload (HMR)
- Component story writing
- Visual regression testing ready
- Design system documentation

### Workflow
```bash
# 1. Start Designer workflow
npm run designer

# 2. Storybook opens automatically
# Open: http://localhost:6006/

# 3. Create/edit components
vim components/web/ui/button.tsx

# 4. Component stories update instantly
# Add story in .stories.tsx files
```

### Best Practices
1. **Create component stories** for every new component
2. **Use dark mode toggle** to test both themes
3. **Test responsive design** in Storybook viewport
4. **Document props** with JSDoc comments
5. **Export all component variants** in stories

---

## PM Workflow

**서비스 플로우 및 통합 개발**

### Command
```bash
npm run pm
```

### Execution Flow
```
1 Lint Check
 ├─ ESLint validation
 ├─ Code style check
 └─ Pass → Continue

2 Type Check
 ├─ TypeScript compilation
 ├─ Type safety validation
 └─ Warnings allowed → Continue

3 Test Suite
 ├─ Integration tests
 ├─ Component integration
 └─ Pass → Continue

4 Dev Server Launch
 ├─ http://localhost:3001/
 ├─ Hot reload enabled
 ├─ Demo page active
 └─ Full component showcase
```

### Features
- Live component testing
- Dark mode toggle
- Real-time updates (HMR)
- Integration ready
- Service flow design

### Workflow
```bash
# 1. Start PM workflow
npm run pm

# 2. Dev server opens
# Open: http://localhost:3001/

# 3. Create/edit service flows
vim flows/my-product/index.tsx

# 4. Test component integration
# Flows update instantly (HMR)

# 5. Verify dark mode
# Toggle / in header
```

### Best Practices
1. **Use all 12 components** in demo app
2. **Test dark mode** for accessibility
3. **Verify responsive design** (mobile, tablet, desktop)
4. **Check component states** (active, disabled, error)
5. **Document integration patterns** in flows

---

## Admin Workflow

**템플릿 및 환경 관리**

### Command
```bash
npm run admin
```

### Execution Flow
```
1 Lint Check 
2 Type Check 
3 Test Suite 
4 Interactive Menu
 ├─ 1. Edit component specs
 ├─ 2. Edit role definitions
 ├─ 3. Update theme
 ├─ 4. Build for production
 ├─ 5. Start dev server
 └─ 6. View Storybook
```

### Features
- Role/permission management
- Theme configuration
- Template updates
- Production builds
- Environment control

### Workflow
```bash
# 1. Start Admin workflow
npm run admin

# 2. Select action from menu
# Options 1-6

# Example: Edit theme
# Select: 3
# Opens: .claude/manifests/theme.yaml

# 3. Update configuration
vim .claude/manifests/theme.yaml

# 4. Rebuild components
npm run build
```

### Best Practices
1. **Backup theme before updates**
2. **Test all components** after theme changes
3. **Verify role permissions** regularly
4. **Document template changes** in CHANGELOG
5. **Test production build** before deploying

---

## Verification Process (All Roles)

### Step 1: Lint Check
```bash
npm run lint
```
**Validates:**
- Code style consistency
- ESLint rules compliance
- No code smells

### Step 2: Type Check
```bash
npm run type-check
```
**Validates:**
- TypeScript compilation
- Type safety
- No type errors

**Note:** Minor type warnings are allowed (non-blocking)

### Step 3: Test Suite
```bash
npm run test
```
**Validates:**
- Component functionality
- Integration tests
- Edge cases

### Step 4: Launch Environment
- **Designer** → Storybook
- **PM** → Dev Server
- **Admin** → Interactive Menu

---

## Package Manager Support

### npm (Current)
```bash
npm install
npm run designer # Works
npm run pm # Works
npm run admin # Works
```

### pnpm (Compatible)
```bash
pnpm install
npm run designer # Works
npm run pm # Works
npm run admin # Works
```

### Configuration
```json
{
 "packageManager": "npm@10.x || pnpm@10.x"
}
```

---

## Quick Reference

### Designer
```bash
npm run designer # Start workflow
# ↓
# Storybook opens (port 6006)
# Edit components/web/ui/*.tsx
# Stories update automatically
```

### PM
```bash
npm run pm # Start workflow
# ↓
# Dev server opens (port 3001)
# Edit src/App.tsx or flows/
# Demo page updates automatically
```

### Admin
```bash
npm run admin # Start workflow
# ↓
# Menu appears (select action)
# 1. Edit specs
# 2. Edit roles
# 3. Update theme
# etc...
```

---

## Manual Verification Only

If you just want to run verification without launching an environment:

```bash
npm run verify
# Runs: lint → type-check → test
# Exits: Does not launch any environment
```

---

## Troubleshooting

### Lint Fails
```bash
# Auto-fix issues
npm run format
# Then retry workflow
npm run designer
```

### Type Check Warnings
```bash
# Warnings are non-blocking
# Review in browser dev tools
# Continue with workflow
```

### Tests Fail
```bash
# Check error message
# Fix issues in code
# Restart workflow
```

### Port Already in Use
```bash
# For Storybook
npm run storybook -- --port 6007

# For Dev Server
npm run dev -- --port 3002
```

---

## File Structure

```
scripts/roles/
├── designer.sh # Designer workflow
├── pm.sh # PM workflow
└── admin.sh # Admin workflow

.npmrc # Package manager config
package.json # Role commands defined
```

---

## Checklist

- [ ] All verifications pass (lint, type-check, test)
- [ ] Environment launches correctly
- [ ] HMR (Hot Module Reload) working
- [ ] Components render properly
- [ ] Dark mode toggles
- [ ] No console errors

---

## Notes

- **Verification is mandatory** before launching environment
- **HMR enabled** in all workflows (auto-reload on file changes)
- **No manual refresh needed** when editing files
- **All ports configurable** if conflicts occur
- **pnpm support ready** (use instead of npm when needed)

---

**Last Updated:** 2026-02-24
**Status:** Production Ready
