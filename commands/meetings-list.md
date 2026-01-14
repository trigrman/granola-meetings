---
description: List recent meetings from Granola
allowed-tools: Bash
---

# List Meetings

List recent meetings from Granola's local cache.

## Usage

```
/granola-meetings:meetings-list [limit]
```

- `limit` (optional): Number of meetings to show (default: 10)

## Instructions

1. Run the granola reader script to list meetings:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py list
   ```

2. Display meetings in a table format with:
   - Date and time
   - Meeting title
   - Meeting ID (for use with other commands)

3. List meetings in chronological order (earliest first)

4. Include timestamps (e.g., "9:00 AM" or "2:30 PM") for each meeting
