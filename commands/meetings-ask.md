---
description: Ask questions about meeting content
allowed-tools: Bash
---

# Ask About Meetings

Search meetings or ask questions about meeting content.

## Usage

```
/granola-meetings:meetings-ask <query>
```

- `query`: Search term or question about meetings

## Instructions

1. Search meetings for the query:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py search "<query>"
   ```

2. If the search returns relevant meetings, retrieve their full notes:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <meeting-id> --transcript
   ```

3. Answer the user's question based on the meeting content.

4. Always cite which meeting(s) the information came from.

## Examples

- "What did we decide about the API design?"
- "What action items came from meetings with Sarah?"
- "When did we last discuss the roadmap?"
