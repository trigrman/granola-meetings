---
description: Get notes from a specific meeting
allowed-tools: Bash
---

# Get Meeting

Retrieve full notes from a specific meeting.

## Usage

```
/granola-meetings:meetings-get <meeting-id> [--transcript]
```

- `meeting-id`: The meeting ID (from meetings-list)
- `--transcript`: Include raw transcript (optional)

## Instructions

1. If no meeting ID provided in arguments, first run:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py list
   ```
   Then ask the user which meeting they want to view.

2. Get the meeting notes:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <meeting-id>
   ```

   Or with transcript:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <meeting-id> --transcript
   ```

3. Display the meeting notes in a readable format.
