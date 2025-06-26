# Functional State Branching Workflow Specification

## Core Rules

1. **The main branch MUST always be in a functional state** - buildable, testable, and runnable.
2. **Direct commits to main ARE THE DEFAULT** for all atomic, non-breaking changes.
3. **Functional state branches MUST be created** when transitions between functional states require multiple commits.
4. **Branch names MUST follow the pattern**: `fs/<change-type>-<description>-<timestamp>`
5. **Every commit MUST leave the codebase in a valid state** within its branch context.
6. **Merges MUST use --no-ff** to preserve branch history.

## Workflow Procedures

### Initial Decision

1. **ANALYZE** the required change
2. **DETERMINE** if the change can be completed in a single atomic commit
3. **CHECK** if the change will temporarily break functionality
4. **PROCEED** to either Direct Commit or Functional State Branch

### Direct Commit Procedure (Default)

```bash
# STAGE your changes
git add <files>

# COMMIT with descriptive message
git commit -m "<type>: <description>"

# PUSH directly to main
git push origin main
```

### Functional State Branch Procedure

```bash
# CREATE functional state branch
git checkout -b fs/<type>-<description>-$(date +%Y%m%d-%H%M%S)

# MAKE series of commits, each with step indicator
git commit -m "<type>(1/n): <description of step 1>"
git commit -m "<type>(2/n): <description of step 2>"
git commit -m "<type>(n/n): <description of final step>"

# PUSH branch
git push origin <branch-name>

# SWITCH to main
git checkout main

# MERGE with no-fast-forward
git merge --no-ff <branch-name>

# PUSH updated main
git push origin main

# DELETE local branch
git branch -d <branch-name>

# DELETE remote branch
git push origin --delete <branch-name>
```

## Decision Criteria

### Use **DIRECT COMMIT** When

- Adding new functions that don't modify existing interfaces
- Fixing bugs in a single commit
- Adding or updating tests
- Updating documentation
- Making style or formatting changes
- Refactoring that maintains all public interfaces

### Use **FUNCTIONAL STATE BRANCH** When

- Breaking changes to public interfaces
- Multi-file refactoring that creates temporary inconsistencies
- Database migrations requiring coordinated changes
- Dependency replacements affecting multiple modules
- API version upgrades with breaking changes
- Any change requiring "temporary breakage"

## Workflow Diagram

```text
┌─────────────────┐
│  Analyze Change │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Single atomic commit?│
│ No breaking changes? │
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌─────────┐ ┌──────────────────┐
│ Direct  │ │ Functional State │
│ Commit  │ │     Branch       │
└────┬────┘ └────────┬─────────┘
     │               │
     │               ▼
     │      ┌─────────────────┐
     │      │ Make commits 1/n │
     │      └────────┬─────────┘
     │               │
     │               ▼
     │      ┌─────────────────┐
     │      │ Make commits 2/n │
     │      └────────┬─────────┘
     │               │
     │               ▼
     │      ┌─────────────────┐
     │      │ Make commits n/n │
     │      └────────┬─────────┘
     │               │
     │               ▼
     │      ┌─────────────────┐
     │      │ Merge to main   │
     │      └────────┬─────────┘
     │               │
     └───────┬───────┘
             │
             ▼
      ┌─────────────┐
      │ Push to main│
      └─────────────┘
```

## Examples

### Example 1: Direct Commit (Adding a feature)

```bash
# Adding a new utility function
git add src/utils/date_formatter.py tests/test_date_formatter.py
git commit -m "feat: Add ISO date formatting utility"
git push origin main
```

### Example 2: Functional State Branch (Replacing ORM)

```bash
# Create branch for ORM replacement
git checkout -b fs/replace-sqlalchemy-with-tortoise-20250612-143000

# Step 1: Add abstraction layer
git add src/db/abstract.py
git commit -m "refactor(1/4): Create database abstraction interface"

# Step 2: Implement new ORM
git add src/db/tortoise_impl.py requirements.txt
git commit -m "refactor(2/4): Add Tortoise ORM implementation"

# Step 3: Update all models
git add src/models/*.py
git commit -m "refactor(3/4): Migrate all models to use abstraction"

# Step 4: Remove old ORM
git rm src/db/sqlalchemy_impl.py
git commit -m "refactor(4/4): Remove SQLAlchemy and update dependencies"

# Push and merge
git push origin fs/replace-sqlalchemy-with-tortoise-20250612-143000
git checkout main
git merge --no-ff fs/replace-sqlalchemy-with-tortoise-20250612-143000
git push origin main
git branch -d fs/replace-sqlalchemy-with-tortoise-20250612-143000
git push origin --delete fs/replace-sqlalchemy-with-tortoise-20250612-143000
```

## State Validation

**BEFORE each commit, verify:**

```bash
# Run tests
pytest

# Check build
python -m build

# Verify no linting errors
ruff check --select E,F,B,I src/
uvx ty src/
```
