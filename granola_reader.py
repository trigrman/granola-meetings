#!/usr/bin/env python3
"""
Granola Meeting Notes Reader
Reads meeting transcripts and AI-generated notes from the local Granola cache.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

GRANOLA_CACHE = Path.home() / "Library/Application Support/Granola/cache-v3.json"


def extract_text_from_content(node) -> list[str]:
    """Recursively extract markdown text from Granola's doc structure."""
    result = []

    if isinstance(node, dict):
        node_type = node.get('type', '')

        if node_type == 'text':
            return [node.get('text', '')]

        if node_type == 'heading':
            level = node.get('attrs', {}).get('level', 1)
            prefix = '#' * level + ' '
            text = ''.join(extract_text_from_content(node.get('content', [])))
            return [f"\n{prefix}{text}\n"]

        if node_type == 'bulletList':
            items = []
            for item in node.get('content', []):
                item_text = ''.join(extract_text_from_content(item)).strip()
                if item_text:
                    items.append(f"- {item_text}")
            return ['\n'.join(items) + '\n']

        if node_type == 'orderedList':
            items = []
            for i, item in enumerate(node.get('content', []), 1):
                item_text = ''.join(extract_text_from_content(item)).strip()
                if item_text:
                    items.append(f"{i}. {item_text}")
            return ['\n'.join(items) + '\n']

        if node_type in ('paragraph', 'listItem'):
            text = ''.join(extract_text_from_content(node.get('content', [])))
            return [text]

        if node_type == 'hardBreak':
            return ['\n']

        if 'content' in node:
            return extract_text_from_content(node['content'])

    elif isinstance(node, list):
        for item in node:
            result.extend(extract_text_from_content(item))

    return result


def get_formatted_notes(state: dict, document_id: str) -> str:
    """Get the AI-generated formatted notes (panels) for a document."""
    panels = state.get('documentPanels', {})
    doc_panels = panels.get(document_id, {})

    if not isinstance(doc_panels, dict):
        return ''

    result = []
    for panel_id, panel in doc_panels.items():
        if isinstance(panel, dict):
            panel_title = panel.get('title', '')
            content = panel.get('content', {})

            if panel_title:
                result.append(f"## {panel_title}\n")

            text_parts = extract_text_from_content(content)
            result.append(''.join(text_parts))

    return '\n'.join(result).strip()


def load_granola_data():
    """Load and parse the Granola cache file."""
    if not GRANOLA_CACHE.exists():
        raise FileNotFoundError(f"Granola cache not found at {GRANOLA_CACHE}")

    with open(GRANOLA_CACHE, 'r') as f:
        data = json.load(f)

    inner = json.loads(data['cache'])
    return inner.get('state', {})


def extract_start_time(doc: dict) -> Optional[str]:
    """Extract meeting start time from google_calendar_event or fall back to created_at."""
    cal_event = doc.get('google_calendar_event')
    if cal_event and isinstance(cal_event, dict):
        start = cal_event.get('start', {})
        if start.get('dateTime'):
            return start['dateTime']
    return doc.get('created_at')


def format_time_display(iso_time: Optional[str]) -> str:
    """Format ISO timestamp to readable time (e.g., '9:00 AM')."""
    if not iso_time:
        return ''
    try:
        # Parse ISO format (handles both Z suffix and timezone offset)
        if 'T' in iso_time:
            # Remove Z suffix or parse with offset
            time_str = iso_time.replace('Z', '+00:00')
            dt = datetime.fromisoformat(time_str)
            return dt.strftime('%-I:%M %p')
    except (ValueError, AttributeError):
        pass
    return ''


def get_documents(state: dict) -> list[dict]:
    """Extract all meeting documents with their notes."""
    docs = state.get('documents', {})
    if not isinstance(docs, dict):
        return []

    results = []
    for doc_id, doc in docs.items():
        if not isinstance(doc, dict):
            continue

        start_time = extract_start_time(doc)
        results.append({
            'id': doc_id,
            'title': doc.get('title', 'Untitled'),
            'created_at': doc.get('created_at'),
            'start_time': start_time,
            'notes_markdown': doc.get('notes_markdown', ''),
            'notes_plain': doc.get('notes_plain', ''),
            'overview': doc.get('overview', ''),
            'summary': doc.get('summary'),
        })

    # Sort by start_time descending (most recent first)
    results.sort(key=lambda x: x.get('start_time') or '', reverse=True)
    return results


def get_transcript(state: dict, document_id: str) -> list[dict]:
    """Get transcript segments for a specific document."""
    transcripts = state.get('transcripts', {})

    # Transcripts are stored as lists keyed by some ID
    for t_id, segments in transcripts.items():
        if isinstance(segments, list):
            doc_segments = [s for s in segments if s.get('document_id') == document_id]
            if doc_segments:
                return sorted(doc_segments, key=lambda x: x.get('start_timestamp', ''))

    return []


def format_transcript(segments: list[dict]) -> str:
    """Format transcript segments into readable text."""
    lines = []
    for seg in segments:
        text = seg.get('text', '').strip()
        if text:
            lines.append(text)
    return ' '.join(lines)


def list_recent_meetings(limit: int = 10) -> list[dict]:
    """List recent meetings with their notes."""
    state = load_granola_data()
    docs = get_documents(state)
    return docs[:limit]


def get_meeting(document_id: str, include_transcript: bool = False) -> Optional[dict]:
    """Get a specific meeting with its formatted notes and optionally transcript."""
    state = load_granola_data()
    docs = state.get('documents', {})

    doc = docs.get(document_id)
    if not doc:
        return None

    result = {
        'id': document_id,
        'title': doc.get('title', 'Untitled'),
        'created_at': doc.get('created_at'),
        'start_time': extract_start_time(doc),
        'formatted_notes': get_formatted_notes(state, document_id),
        'overview': doc.get('overview', ''),
        'summary': doc.get('summary'),
    }

    if include_transcript:
        transcript_segments = get_transcript(state, document_id)
        result['transcript'] = format_transcript(transcript_segments)

    return result


def get_recent_meetings_with_notes(limit: int = 5) -> list[dict]:
    """Get recent meetings with their full formatted notes."""
    state = load_granola_data()
    docs = get_documents(state)

    results = []
    for doc in docs[:limit]:
        results.append({
            'id': doc['id'],
            'title': doc['title'],
            'created_at': doc['created_at'],
            'formatted_notes': get_formatted_notes(state, doc['id']),
        })

    return results


def search_meetings(query: str) -> list[dict]:
    """Search meetings by title or content."""
    state = load_granola_data()
    docs = get_documents(state)
    query_lower = query.lower()

    results = []
    for doc in docs:
        searchable = f"{doc.get('title', '')} {doc.get('notes_plain', '')} {doc.get('overview', '')}".lower()
        if query_lower in searchable:
            results.append(doc)

    return results


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: granola_reader.py [list|notes [limit]|search <query>|get <id> [--transcript]]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'list':
        meetings = list_recent_meetings()
        # Group by date and sort each day chronologically (earliest first)
        from collections import defaultdict
        by_date = defaultdict(list)
        for m in meetings:
            start = m.get('start_time') or m.get('created_at') or ''
            date = start[:10] if start else 'Unknown'
            by_date[date].append(m)

        # Sort dates descending, but meetings within each date ascending (chronological)
        for date in sorted(by_date.keys(), reverse=True):
            day_meetings = sorted(by_date[date], key=lambda x: x.get('start_time') or x.get('created_at') or '')
            for m in day_meetings:
                time_display = format_time_display(m.get('start_time'))
                time_str = f" {time_display}" if time_display else ""
                print(f"[{date}{time_str}] {m['title']}")
                print(f"  ID: {m['id']}")
                print()

    elif cmd == 'notes':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        meetings = get_recent_meetings_with_notes(limit)
        for m in meetings:
            date = m.get('created_at', '')[:10] if m.get('created_at') else 'Unknown'
            print(f"# {m['title']} ({date})\n")
            if m.get('formatted_notes'):
                print(m['formatted_notes'])
            else:
                print("(No formatted notes available)")
            print("\n" + "=" * 60 + "\n")

    elif cmd == 'search' and len(sys.argv) > 2:
        query = ' '.join(sys.argv[2:])
        results = search_meetings(query)
        print(f"Found {len(results)} meetings matching '{query}':\n")
        for m in results:
            print(f"- {m['title']} ({m.get('created_at', '')[:10]})")
            print(f"  ID: {m['id']}")

    elif cmd == 'get' and len(sys.argv) > 2:
        doc_id = sys.argv[2]
        include_transcript = '--transcript' in sys.argv
        meeting = get_meeting(doc_id, include_transcript=include_transcript)
        if meeting:
            print(f"# {meeting['title']}")
            start = meeting.get('start_time') or meeting.get('created_at') or ''
            date = start[:10] if start else 'Unknown'
            time_display = format_time_display(meeting.get('start_time'))
            time_str = f" at {time_display}" if time_display else ""
            print(f"Date: {date}{time_str}\n")
            if meeting.get('formatted_notes'):
                print(meeting['formatted_notes'])
            if meeting.get('transcript'):
                print(f"\n## Raw Transcript\n{meeting['transcript'][:3000]}...")
        else:
            print(f"Meeting {doc_id} not found")

    else:
        print("Usage: granola_reader.py [list|notes [limit]|search <query>|get <id> [--transcript]]")
