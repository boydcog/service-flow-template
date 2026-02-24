# Service Flow Template —  

  2026-02-24  **Phase 1-3 ** .

---

## 

    5   :

1.  ** ** ( )
2.  **Startup ** (     )
3.  **PR  ** ( )
4.  **  UI** (  )
5.  **Admin ** (   )

---

##    

```
.claude/
 migrations/
    v1-to-v2.sh                
 hooks/
    startup.sh                 (  )
    create-pr.sh              PR  
    check-status.sh             UI
    admin-workflow.sh         Admin 
 IMPLEMENTATION.md              
```

---

##  Phase 1:  

### 
- **  **: `.user-identity`, `.gh-token` gitignore 
- **  **:       
- ** **: gitignore      

###  

#### `.claude/state/_schema_version.txt`
```
v1  ←  
```

#### `.claude/migrations/_target_version.txt`
```
v1  ←   (v1   )
```

#### `.claude/migrations/v1-to-v2.sh`
 .   :
1. `.user-identity` git skip-worktree 
2. `.gh-token`   ( )
3. `flows/`  
4. `.claude/state/` 

###  

####   ()
```bash
#     
# startup.sh   →  
```

####  
```bash
bash .claude/migrations/v1-to-v2.sh
```

###   (v2 → v3)
```bash
# 1.    
cat > .claude/migrations/v2-to-v3.sh <<EOF
#!/bin/bash
# v2 to v3 
...
EOF

# 2.   
echo "v3" > .claude/migrations/_target_version.txt

# 3.      
```

---

##  Phase 2: Startup 

### 

:
```bash
#    
WARN MIGRATION_NEEDED: v1 → v2
```

 :
```bash
#    
  : v1 → v2
  ...
  
```

###  

```
 
  ↓
1.   
2. GH  
3.    (git skip-worktree)
4. Git pull
5. ** **
   →   
6.  
7.  
```

###  
```bash
#  
cat .claude/state/logs/migrations.log

# :
# [2026-02-24 16:55:32] Migration v1→v2 completed
```

---

##  Phase 2+3: PR   &  

###  

####  1: Admin    PR 

```bash
# 1.     (  )

# 2. Admin  
bash .claude/hooks/admin-workflow.sh \
    " " \
    " (designer) " \
    ""

# :
#   : admin/1708741600
#  CHANGELOG  ...
#  CHANGELOG 
#    ...
#  PR  : [admin] :  
#  PR  !
#  PR URL: https://github.com/anthropics/service-flow-template/pull/123
```

####  2:   

```bash
#    
bash .claude/hooks/check-status.sh

#    
bash .claude/hooks/check-status.sh --pr       # PR 
bash .claude/hooks/check-status.sh --branch   #  
bash .claude/hooks/check-status.sh --local    #  
```

###  

#### `.claude/hooks/create-pr.sh`
PR   

```bash
# 
bash .claude/hooks/create-pr.sh <branch> <title> [description]

# 
bash .claude/hooks/create-pr.sh \
    "component/button" \
    "[designer] : Button " \
    "   ..."
```

:
-   
-  GH_TOKEN 
-  git push 
-  PR 
-  PR  
-  PR  

#### `.claude/hooks/check-status.sh`
    UI

```bash
#   
bash .claude/hooks/check-status.sh

#  :
# ========================================
# Service Flow Template —  
# ========================================
#
#   
#
#  :
#   3f7a8c2 admin:  
#   b4d5e1f admin:  
#   c6f9g2h [designer]  
#
#  :
#  manifests/team.yaml | 2 ++
#  1 file changed, 2 insertions(+)
#
#   
#
#  : admin/1708741600
#    (): 1
#  main  
#
#  PR  
#
# PR #123: [admin] :   [OPEN]
#
#    PR
#
# PR #122: [designer] : Button  (: 2026-02-24)
#
#   
#
#  : v1
#  : v1
#    
```

#### `.claude/hooks/admin-workflow.sh`
Admin   (  →  → PR )

```bash
bash .claude/hooks/admin-workflow.sh <action> <description> [user]

# 
bash .claude/hooks/admin-workflow.sh \
    " " \
    " (designer) " \
    ""
```

:
-    
-  CHANGELOG 
-   
-  PR  
-    

---

##    (Admin )

### Before ()
```
1.   ( main )
2. git add / commit / push ()
3. GitHub PR  ()
4.   (GitHub )
5.  pull ()
```

 ****:
- GitHub   
-     
-   

### After ()
```
1.  
2. bash .claude/hooks/admin-workflow.sh "" ""
3. bash .claude/hooks/check-status.sh  #  
4.       
```

 ****:
- GitHub   
- CLI   
-  
-      

---

##    (Phase 4)

###    

1. **Designer   **
   - `/designer`    PR 
   - Storybook  

2. **Flow   **
   - `/flow`    PR 
   - Dev   

3. **   (Intent Detection)**
   -    →    
   - CLAUDE.md "  →  " 

###   (v1 → v2 → v3)

    :
```bash
# v2 → v3  
cat > .claude/migrations/v2-to-v3.sh <<EOF
#!/bin/bash
#   
EOF

echo "v3" > .claude/migrations/_target_version.txt
```

---

##  

 :

- [ ] `.claude/migrations/v1-to-v2.sh`   (755)
- [ ] `.claude/hooks/startup.sh`   
- [ ] `.claude/hooks/create-pr.sh`  
- [ ] `.claude/hooks/check-status.sh`  
- [ ] `.claude/hooks/admin-workflow.sh`  
- [ ] `GH_TOKEN` 
- [ ] `.user-identity`  
- [ ]      

---

##   

- `.claude/CLAUDE.md` —    ( )
- `.claude/manifests/` — , ,  
- `.claude/state/` —   
- `CHANGELOG.md` —  

---

##  

### 

```bash
#   
tail -f .claude/state/logs/migrations.log

# PR  
cat .claude/state/logs/pr-history.log

# Admin   
cat .claude/state/logs/admin-actions.log
```

###    

```bash
#     
echo "v1" > .claude/state/_schema_version.txt

#     
bash .claude/migrations/v1-to-v2.sh
```

---

##  FAQ

### Q: PR   "GitHub    " 

**A**: `.gh-token`   .
```bash
# /setup  
echo "your-github-token" > .claude/.gh-token
chmod 600 .claude/.gh-token
```

### Q:    

**A**: `.claude/migrations/_target_version.txt`  .
```bash
#  
cat .claude/state/_schema_version.txt

#  
cat .claude/migrations/_target_version.txt

#   
```

### Q: Admin      

**A**: `admin-workflow.sh` `git add -A`   .     :
```bash
#  
git add manifests/team.yaml
git commit -m "admin:  "
bash .claude/hooks/create-pr.sh admin/xxxxx "[admin] :  "
```

---

##   

  `set -euo pipefail`       .

 :
1.   
2. `.claude/state/logs/`   
3. `git status` 
4.    

---

 : 2026-02-24
