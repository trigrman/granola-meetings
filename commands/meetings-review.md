---
description: Review meetings for action items and create tasks
allowed-tools: Bash, Read, Write, Edit
---

# Review Meetings

Review unreviewed meetings to extract action items and create tasks. Integrates with the task-management plugin.

## Dependencies

This command requires the `task-management` plugin to be installed and configured.

## Usage

```
/granola-meetings:meetings-review [--all]
```

- `--all`: Review all recent meetings, not just unreviewed ones

## Instructions

### Step 1: Load Configuration

1. Read the task-management config to find the tasks root:
   ```bash
   cat ~/.claude/task-management-config/config.yaml
   ```

2. Extract the `tasks_root` path from the config.

### Step 2: Get Reviewed Meetings

1. Check for the reviewed meetings file at `{tasks_root}/memories/reviewed-meetings.md`

2. If it exists, read it to get the list of already-reviewed meeting IDs.

3. If it doesn't exist, treat all meetings as unreviewed.

### Step 3: Get Recent Meetings

1. List recent meetings from Granola:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py list
   ```

2. Filter out meetings that have already been reviewed (unless `--all` flag is used).

3. If no unreviewed meetings, inform the user and exit.

### Step 4: Review Each Meeting

For each unreviewed meeting:

1. Get the full meeting notes:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/granola_reader.py get <meeting-id>
   ```

2. Analyze the notes to extract:
   - **Action items for Mike**: Tasks, follow-ups, commitments Mike made or was assigned
   - **Important decisions**: Key decisions that might be worth remembering
   - **Context/people notes**: Important information about people, projects, or relationships

3. Present findings to the user:
   ```
   ## Meeting: [Title] - [Date]

   ### Proposed Tasks
   - [ ] Task 1 (due: suggested date)
   - [ ] Task 2

   ### Potential Memories
   - Decision about X
   - Context about Y
   ```

### Step 5: Get User Approval

For each meeting's findings:

1. Ask the user which items to create:
   - Which tasks to add to import/?
   - Which items to add to memories/?
   - Any modifications needed?

2. Only create items the user explicitly approves.

### Step 6: Create Approved Items

For approved tasks:

1. Create task files in `{tasks_root}/import/` with frontmatter:
   ```yaml
   ---
   type: task
   due: YYYY-MM-DD
   tags: [from-meeting]
   source: meeting
   ---
   # Task Title

   Task description

   **Source:** [Meeting Title] ([Date])
   ```

For approved memories:

1. Create or append to memory files in `{tasks_root}/memories/`

### Step 7: Update Reviewed Meetings

1. Add the reviewed meeting IDs to `{tasks_root}/memories/reviewed-meetings.md`:
   ```markdown
   ---
   type: memory
   ---
   # Reviewed Meetings

   Meeting IDs that have been reviewed for action items.

   ## Reviewed

   - [Meeting ID] - [Date] - [Title]
   ```

## Notes

- Always ask for approval before creating any tasks or memories
- Suggest reasonable due dates based on meeting context (e.g., "follow up next week")
- Use `from-meeting` tag to identify tasks that came from meeting review
- Include meeting source in task description for context
