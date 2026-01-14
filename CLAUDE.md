# Granola Meetings Plugin

## Overview

Claude Code plugin for accessing and reviewing meeting notes from Granola. Integrates with the task-management plugin to extract action items and create tasks.

## Plugin Structure

```
granola-meetings/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   ├── meetings-list.md     # /granola-meetings:meetings-list
│   ├── meetings-get.md      # /granola-meetings:meetings-get
│   ├── meetings-ask.md      # /granola-meetings:meetings-ask
│   └── meetings-review.md   # /granola-meetings:meetings-review
├── skills/
│   └── meetings/
│       └── SKILL.md         # Shared meeting context
├── granola_reader.py        # Python script for reading Granola cache
└── CLAUDE.md
```

## Local Development

Test the plugin locally:
```bash
claude --plugin-dir ~/dev/granola-meetings
```

Commands will be available as:
- `/granola-meetings:meetings-list`
- `/granola-meetings:meetings-get`
- `/granola-meetings:meetings-review`
- `/granola-meetings:meetings-ask`

## Dependencies

- **task-management plugin** (soft dependency): Used by the meetings-review command
  - Not enforced by the plugin system, but meetings-review will fail without it
  - Reads config from `~/.claude/task-management-config/config.yaml`
  - Stores reviewed meeting state in `{tasks_root}/memories/`
  - Creates tasks in `{tasks_root}/import/`

## Data Source

- Granola cache: `~/Library/Application Support/Granola/cache-v3.json`
- Meeting times come from `google_calendar_event.start.dateTime`
- Falls back to `created_at` if no calendar event
