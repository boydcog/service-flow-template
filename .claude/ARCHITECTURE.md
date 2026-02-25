# Service Flow Template — & 

## 

** (Git), ()**

- **** (Git ): , , 
- **** (Git ): , , Agent Team 

---

## 

### (Git )

```
.claude/
 commands/ ← Skill 
 hooks/ ← 
 manifests/ ← 
 team.yaml Admin (/)
 roles.yaml Admin ()
 theme.yaml Admin (Emocog )
 spec/ ← 
 component-spec.md
 flow-spec.md
 migrations/ ← 

components/
 web/ui/ ← 
 native/ui/ ← 

CLAUDE.md ← (Intent Detection, )
package.json ← 
```

### (Git )

```
flows/ ← 
 .gitignore # flows/ 
 product-a/
 screens/
 navigation/
 data-flow/
 product-b/
 ...

projects/ ← 
 .gitignore # projects/ 
 product-a/
 src/
 tests/
 .claude/
 state/ # state
 agents/ # Agent Team 
 orchestration/ # 
 package.json
 product-b/
 ...

.claude/state/ ← (Git )
 _schema_version.txt
 _active_flow.txt
 logs/ # /PR 
 pids/ # ID
```

---

## 

### Admin/Developer ( )

** ** ( ):
```
Admin → team.yaml ( /)
 → roles.yaml ( )
 → theme.yaml ( )
 → manifests/* ( )
 → spec/* ( )
 → components/* ( )
 → CLAUDE.md ( )
```

****:
1. Admin (: team.yaml )
2. `/admin` → PR 
3. PR → 
4. → 

### Designer ( )

** ** ( ):
```
Designer → components/web/button.tsx
 → components/native/Button.tsx
 → ( )
```

** ** ( ):
```
projects/product-a/
 src/components/ ← 
 ...
```

### PM ( )

** ** ( ):
```
PM → flows/product-a/
 → flows/product-b/
 → ( , Git )
```

** **:
```
projects/product-a/
 src/
 .claude/orchestration/ ← Agent Team 
 ...
```

---

## 

### Admin 

```
Timeline:


Admin User Session 1:
 1. /admin 
 2. team.yaml ( )
 3. PR → 
 4. main 

Designer Session (5 ):
 1. → startup.sh 
 2. git pull team.yaml 
 3. load team.yaml 
 4. verify_permissions() 
 5. Intent Detection 
```

### 

```
Product A Development:
 - flows/product-a/
 - projects/product-a/
 - Agent Team 
 → .gitignore ()
 → Git 
 → 

Product B Development:
 - flows/product-b/
 - projects/product-b/
 - 
 → flows/product-a 
```

---

## 

### Admin 

- [ ] team.yaml 
- [ ] roles.yaml 
- [ ] theme.yaml 
- [ ] spec/ 
- [ ] → `/admin` → PR → 

### Startup.sh 

- [ ] git pull ( )
- [ ] load team.yaml + roles.yaml
- [ ] verify_permissions() ( )
- [ ] 

### .gitignore 

- [ ] flows/* ( )
- [ ] projects/* ( )
- [ ] .claude/state/* ( )
- [ ] .user-identity, .gh-token ( )

---

## 

### Admin 

Admin → team.yaml → PR → ** ** 

### 

 → Git → ** ** 

### " "

```
 (Git):
 (CLAUDE.md)
 (spec/)
 (team.yaml)
 (roles.yaml)
 (theme.yaml)
 (components/)

 ():
 (projects/)
 (flows/)
 Agent Team 

```

---

## 

### 

1. **Startup team.yaml + roles.yaml **
 ```bash
 # startup.sh 
 load_team_config()
 load_roles_config()
 verify_permissions()
 ```

2. **Intent Detection **
 ```
 → → ? → Skill 
 ```

3. ** **
 ```
 /flow {product-name}
 → flows/{product-name}/ 
 → projects/{product-name}/ ()
 ```

---

 : 2026-02-24
