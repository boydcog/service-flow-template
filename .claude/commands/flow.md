# /flow —    (Agent Team )

## 

**PM, Designer, Developer     ·.**

- (PM)  
- Designer   
- Developer  
-     →   → PR

****:   (admin, developer, designer, pm)

****:
-     
-    
-   
- PR  

---

## Claude  

    Claude   :

1.   :
   - `.user-identity`    
   -  Skill("setup")  
   - Git : `git pull --rebase`

2.   (AskUserQuestion):
   - : user-onboarding, payment-flow, product-dashboard
   -        

3.   :
   - `git checkout -b flow/{product-name}` (main )

4.    ( ):
   -  /  

5.   :
   - `scan_available_components()` 
   - `components/web/ui/*.tsx`  24  
   -   exports, variants, sizes  
   -     

6.    :
   - `map_components_to_screens()` 
   -    (COMPONENT_KEYWORDS )
   -  (header/navbar/sidebar)  1 
   -   fallback(card + button)  
   -    2  

7.   :
   - `create_page_with_components()`    TSX  
   - import : `@components/web/ui/{name}`
   -  import JSX  1  
   - flows/{product-name}/screens/Screen{N}.tsx 
   - flows/{product-name}/page.tsx (  )

8.   (verify_flow.run_all):
   - import   
   - import   ( import )
   -    
   - TypeScript   0 (npx tsc --noEmit)
   -  3 ,   PR  

9.   (  ):
   -  3000    ( )
   -   
   -  http://localhost:3000 

10.    PR :
    - : [flow] {}: {product-name}  
    - flows/ .gitignore : `git update-index --no-skip-worktree flows/`
    - PR  

---

## 

```mermaid
graph TB
    A[" PM  "] -->|step 1| B["Orchestrator<br/> "]
    B -->| | C[" Designer Agent"]
    B -->| | D[" Developer Agent"]
    B -->| | E["PM Agent<br/>"]

    C -->| | F[" Feedback<br/>"]
    D -->| | F
    E -->| | F

    F -->|| G["  "]
    G -->|YES| H[" "]
    G -->|NO| B

    H -->|dev server| I[" localhost:3000<br/> "]
    I -->|| J[" "]
    J -->|YES| K["PR "]
    J -->|NO| B
```

---

##  

### 1:  

```
 :  (pm)
 :   
```

### 2:  

```
    (: my-awesome-app):
> user-onboarding
```

**  **:
```
 flow/user-onboarding   (main )
```

### 3:    ()

```
    :
>     
> 1)   → 
> 2)    (, )
> 3)   
> 4)   
> 5)     

 5 ,  .
```

### 4:  

```
   ...

1⃣   1:  
==================

 :
> Email Signup

 :
>      

 :
- Input ()
- Button ()
- Text ()

   !

   :
  - Input.tsx (components/web/Input.tsx)
  - Button.tsx (components/web/Button.tsx)

 :
  1. Input ( )
  2. Button ( )
  3. Card ()

 ? (y/n):
> n

2⃣   2:  
==================

 :
> Profile Information

 :
>     (, )

 :
- Input ()
- FileInput ()
- Button ()
- Card ()

[...]
```

### 5:  

```
   ...

 :
  1.  (Linear) — /   ()
  2.  (Tabs) —  
  3.  (Modals) —  
  4.  (Mixed) —   

:
> 1

  :
Screen 1 → Screen 2 → Screen 3 → Screen 4 → Screen 5

    ? (y/n):
> n

  :
  1. Context API + Hooks
  2. LocalStorage
  3. 

:
> 1
```

### 6:   

```
   ...

1⃣    (Context):

formData:
  - email: string
  - name: string
  - photo: File
  - planType: 'free' | 'premium'
  - paymentInfo: { ... }

currentStep: number

2⃣  API :

POST /api/signup
  Input: { email, name, photo }
  Output: { userId, token }

POST /api/confirm-subscription
  Input: { userId, planType, paymentInfo }
  Output: { subscriptionId }

3⃣   :
-   formData 
-      
-      
```

### 7:  

```
  ...

 :
   flow/user-onboarding/page.tsx
   flow/user-onboarding/layout.tsx
   flow/user-onboarding/contexts/FlowContext.tsx
   flow/user-onboarding/types/index.ts
   flow/user-onboarding/screens/Screen1.tsx
   flow/user-onboarding/screens/Screen2.tsx
   flow/user-onboarding/screens/Screen3.tsx
   flow/user-onboarding/screens/Screen4.tsx
   flow/user-onboarding/screens/Screen5.tsx
   flow/user-onboarding/hooks/useNavigation.ts
   flow/user-onboarding/README.md

========================
  !

 : flows/user-onboarding/
  : 11

 :
flows/user-onboarding/
 page.tsx
 layout.tsx
 contexts/
    FlowContext.tsx
 types/
    index.ts
 screens/
    Screen1.tsx
    Screen2.tsx
    Screen3.tsx
    Screen4.tsx
    Screen5.tsx
 hooks/
    useNavigation.ts
 README.md
```

### 8:    ()

```
   ? (y/n):
> y

   ...
 http://localhost:3000   

    !
```

### 9: PR 

```
 PR  ...

1⃣  PR :
: [flow] : user-onboarding  
: flow/user-onboarding → main

2⃣   :
- flows/user-onboarding/* (11 )

3⃣  PR :
 ? (y/n): n
 ? (y/n): n
 ? (y/n): n

========================
 PR !

 PR : https://github.com/{owner}/{repo}/pull/456
 : Open (  )

     .
```

---

##   PR 

###  

```
main ( +  )
 flow/user-onboarding ( )
 flow/payment-flow ( )
 flow/product-dashboard ( )
```

### PR  

1. ** **: `flow/{product-name}`  
2. **PR **:  PR 
3. ****: admin/developer  
4. ****:   
5. ****: main  

### flows/ gitignore 

- **main**: `flows/` `.gitignore`  (  )
- **flow/* **: `flows/`  (git )

**  ( )**:
```bash
git update-index --no-skip-worktree flows/
```

---

##   

### 1. Root Page (`page.tsx`)

```typescript
'use client'

import React from 'react'
import { FlowProvider } from './contexts/FlowContext'
import ScreenContainer from './components/ScreenContainer'

export default function FlowPage() {
  return (
    <FlowProvider>
      <ScreenContainer />
    </FlowProvider>
  )
}
```

### 2. Context (`contexts/FlowContext.tsx`)

```typescript
import React, { createContext, useContext, useState } from 'react'

interface FlowContextType {
  currentStep: number
  formData: Record<string, any>
  navigateTo: (step: number) => void
  updateFormData: (data: Partial<FlowContextType['formData']>) => void
}

const FlowContext = createContext<FlowContextType | undefined>(undefined)

export const FlowProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // ... 
}
```

### 3. Screens (`screens/Screen*.tsx`)

```typescript
'use client'

import React from 'react'
import { useFlow } from '../contexts/FlowContext'
import { Input, Button, Card } from '@/components/web'

export default function Screen1() {
  const { updateFormData, navigateTo } = useFlow()
  const [email, setEmail] = React.useState('')

  const handleNext = () => {
    updateFormData({ email })
    navigateTo(1)
  }

  return (
    <Card>
      <h1> </h1>
      <Input
        type="email"
        placeholder=" "
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button onClick={handleNext}></Button>
    </Card>
  )
}
```

---

##  

###   

-     
-  / 
-  Context 
-   
-  

###   

-     
-   
-      
-   
-  

---

## 

  :

- [ ]   
- [ ] Context   
- [ ]  
- [ ]   
- [ ] API   ( )
- [ ]   
- [ ]   
- [ ] (ARIA) 
- [ ] README.md 
- [ ] PR  

---

## 

- [ ](../spec/flow-spec.md)
- [ ](../spec/component-spec.md)
- [PR ](../templates/pr-template.md)
- [Next.js App Router](https://nextjs.org/docs/app)
- [React Context API](https://react.dev/reference/react/useContext)
