# Agent Skills - Claude Code

> Source: https://code.claude.com/docs/en/skills
> Scraped: 2025-12-13

Agent Skills are modular capabilities that extend Claude's functionality. They are model-invoked (Claude decides when to use them) unlike commands (user-invoked).

## Key Characteristics

- **Model-invoked**: Claude autonomously decides when to use them
- **Composed of**: Required `SKILL.md` plus optional supporting files
- **Three sources**: Personal Skills, Project Skills, Plugin Skills

## Creating Skills

### Storage Locations

**Personal Skills** (`~/.claude/skills/`):
```bash
mkdir -p ~/.claude/skills/my-skill-name
```

**Project Skills** (`.claude/skills/`):
```bash
mkdir -p .claude/skills/my-skill-name
```

## SKILL.md Structure

```yaml
---
name: your-skill-name
description: Brief description of what & when to use
---

# Your Skill Name

## Instructions
Clear, step-by-step guidance for Claude.

## Examples
Concrete examples of using this Skill.
```

### Field Requirements

| Field | Requirements |
|-------|--------------|
| `name` | Lowercase, numbers, hyphens (max 64 chars) |
| `description` | What & when to use (max 1024 chars) |

### Optional: allowed-tools

Restrict which tools Claude can use:
```yaml
---
name: safe-file-reader
description: Read files without making changes.
allowed-tools: Read, Grep, Glob
---
```

## Supporting Files

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional)
├── examples.md (optional)
├── scripts/
│   └── helper.py
└── templates/
    └── template.txt
```

## Best Practices

### 1. Keep Skills Focused
One Skill = one capability
- ✓ "PDF form filling"
- ✓ "Git commit messages"
- ✗ "Document processing" (too broad)

### 2. Write Clear Descriptions
Include what AND when:
```yaml
description: Analyze Excel spreadsheets and create pivot tables. Use when working with .xlsx files or tabular data.
```

### 3. Document Versions
```markdown
## Version History
- v2.0.0 (2025-10-01): Breaking changes
- v1.0.0 (2025-09-01): Initial release
```

## Examples

### Simple Skill
```yaml
---
name: generating-commit-messages
description: Generates clear commit messages. Use when writing commits.
---

# Generating Commit Messages

## Instructions
1. Run `git diff --staged` to see changes
2. Suggest commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components
```

### Skill with Tool Permissions
```yaml
---
name: code-reviewer
description: Review code for best practices. Use for code review.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist
1. Code organization
2. Error handling
3. Performance
4. Security
5. Test coverage
```

## Sharing Skills

### Via Plugins (Recommended)
1. Create plugin with `skills/` directory
2. Add to marketplace
3. Team installs plugin

### Via Git
```bash
mkdir -p .claude/skills/team-skill
# Create SKILL.md
git add .claude/skills/
git commit -m "Add team Skill"
git push
```

## Troubleshooting

### Skill Not Used?
1. Check description specificity
2. Verify file path
3. Validate YAML syntax

### Multiple Skills Conflict?
Use distinct trigger terms in descriptions.
