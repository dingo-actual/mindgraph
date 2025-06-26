# Git Workflow Quick Reference

## Full Git Workflow Guide

If you're unclear about any points relating to the Git workflow or the correct commands to use, you must read claude_handbook/reference/git.md immediately.

## A. Git Commands Reference

### Basic Operations

```bash
git add <file>                 # Stage specific file
git add .                      # Stage all changes
git commit -m "<message>"      # Commit with message
git push origin <branch>       # Push branch to remote
git checkout <branch>          # Switch branches
git checkout -b <new-branch>   # Create and switch to new branch
```

### Branch Operations

```bash
git branch                     # List local branches
git branch -d <branch>         # Delete local branch
git push origin --delete <br>  # Delete remote branch
git merge --no-ff <branch>     # Merge preserving branch history
git log --graph --oneline      # View branch history
```

### Status and History

```bash
git status                     # Show working tree status
git log --oneline -n 10        # Show last 10 commits
git diff                       # Show unstaged changes
git diff --staged              # Show staged changes
```

## B. Branch Timeline Diagrams

### Direct Commit Flow

```text
main: ──●──●──●──●──●──●──●──
         │  │  │  │  │  │  │
         └──┴──┴──┴──┴──┴──┴── All commits directly to main
```

### Functional State Branch Flow

```text
main: ──●──●──●──────────●──●──
              │          │
   fs/change: └──●──●──●─┘
                 1  2  3
                 
● = commit
──── = branch timeline
```

## C. Commit Message Format

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `test`: Test additions/modifications
- `docs`: Documentation changes
- `chore`: Maintenance tasks

### For Functional State Branches

```text
<type>(n/total): <description of this step>
```

## D. Decision Flow Diagram

```text
┌──────────────────────┐
│ Will change break    │
│ existing functionality? │
└───────────┬──────────┘
            │
      ┌─────┴─────┐
      │           │
     NO          YES
      │           │
      ▼           ▼
┌──────────┐  ┌─────────────────────┐
│  DIRECT  │  │ Can it be fixed in  │
│  COMMIT  │  │ a single commit?    │
└──────────┘  └──────────┬──────────┘
                         │
                   ┌─────┴─────┐
                   │           │
                  YES         NO
                   │           │
                   ▼           ▼
             ┌──────────┐  ┌────────┐
             │  DIRECT  │  │ CREATE │
             │  COMMIT  │  │ BRANCH │
             └──────────┘  └────────┘
```

## E. Branch Naming Examples

```text
fs/refactor-api-versioning-20250612-091523
fs/migrate-postgres-to-mysql-20250612-134500
fs/replace-auth-jwt-to-oauth-20250612-160000
fs/update-dependency-major-version-20250612-103045
```

## F. Validation Checklist

**Before EVERY atomic commit:**

- [ ] Tests pass (`pytest`)
- [ ] Code builds (`uv build`)
- [ ] Linting passes (`ruff`, `ty`)
- [ ] Commit message follows format
- [ ] Changes are atomic and complete

**Before merging FS branch:**

- [ ] All commits in sequence complete
- [ ] Final state is fully functional
- [ ] No conflicts with main
