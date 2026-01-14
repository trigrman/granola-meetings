---
name: meetings
description: Access Mike's meeting notes from Granola. Use when asked about meetings, action items, discussions, or to recall what was said in a meeting.
allowed-tools: Bash, Read
---

# Meetings Skill

Reads AI-formatted meeting notes from Granola's local cache.

## Script Location

```
${CLAUDE_PLUGIN_ROOT}/granola_reader.py
```

## Commands

```bash
# List recent meetings
python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py list

# Show formatted notes from last N meetings
python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py notes [limit]

# Get a specific meeting by ID
python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <id>

# Get meeting with raw transcript
python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <id> --transcript

# Search meetings by keyword
python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py search <query>
```

## Display Preferences

When displaying multiple meetings:
- Always list meetings in chronological order (earliest first)
- Include a timestamp for each meeting (e.g., "9:00 AM" or "2:30 PM")
- This ensures Mike can quickly verify the meetings are the expected ones

## Data Source

- Granola cache: `~/Library/Application Support/Granola/cache-v3.json`
- Meeting times come from `google_calendar_event.start.dateTime`
- Falls back to `created_at` if no calendar event

## Integration with task-management

This plugin integrates with the `task-management` plugin:
- Reads config from `~/.claude/task-management-config/config.yaml`
- Stores reviewed meeting state in `{tasks_root}/memories/reviewed-meetings.md`
- Creates tasks from action items in `{tasks_root}/import/`

## Notes

- Data comes from Granola's local cache file
- Only contains meetings that have been synced to the desktop app
- Notes are AI-generated summaries based on the template selected in Granola
