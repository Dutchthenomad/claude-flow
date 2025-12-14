# Skills - Agent Context

## Purpose
This folder contains **agent skills** - model-invoked capabilities that Claude autonomously uses based on context. Unlike commands (user-invoked), skills are triggered automatically when relevant.

## Contents
| Skill | Description |
|-------|-------------|
| `workflow-methodology/` | Core development methodology (TDD, debugging, verification) |

## Integration Points
- Skills are discovered via `SKILL.md` files in subdirectories
- Skills can include supporting files (scripts, templates, references)
- Skills are invoked via the `Skill` tool based on task context
- Skills can restrict tools via `allowed-tools:` frontmatter

## Development Status
- [x] Initial structure
- [ ] Core methodology skill
- [ ] Skill documentation
- [ ] Integration tests
- [ ] Production ready

## For Future Agents
When creating skills:
1. Create a subdirectory with the skill name
2. Include a `SKILL.md` with required frontmatter (`name`, `description`)
3. Keep skills focused on ONE capability
4. Use descriptive trigger terms in the description
5. Include examples in the skill file
6. Add supporting files for complex skills
