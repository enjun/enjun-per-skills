---
name: gt
description: Git workflow automation - automated add/commit/push with auto-generated commit messages.
disable-model-invocation: true
---

# Git Workflow Automation

Quick git add/commit/push workflow.

## Workflow

Execute steps sequentially without asking:

### 1. Stage all changes
! git add -A

### 2. Show status
! git status
! git diff --cached --stat

### 3. Generate commit message

Analyze changes briefly, then create message following this format:
- First line: imperative mood, <50 chars
- (Optional) blank line + details
- Always end with: `Co-Authored-By: Claude`

### 4. Commit
! git commit -m "<message>"

### 5. Push
! git push

## Error Handling

- Nothing to commit: Exit gracefully
- Push rejected: Tell user to pull first
- Other errors: Show error and stop
