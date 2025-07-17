from typing import Dict, List, Optional
from .schemas import Note

class InMemoryNoteStorage:
    """
    In-memory storage backend for notes. 
    Not thread-safe and should be replaced with a DB for production systems.
    """
    def __init__(self):
        self._notes: Dict[int, Note] = {}
        self._id_counter: int = 1

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """Return all notes."""
        return list(self._notes.values())

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Note]:
        """Get a note by its ID."""
        return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def create_note(self, content: str) -> Note:
        """Create a new note and add to storage."""
        note = Note(id=self._id_counter, content=content)
        self._notes[self._id_counter] = note
        self._id_counter += 1
        return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, content: Optional[str] = None) -> Optional[Note]:
        """Update an existing note; only content can be updated."""
        note = self._notes.get(note_id)
        if note is None:
            return None
        if content is not None:
            note.content = content
        return note

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by its ID. Returns True if deleted, False if not found."""
        return self._notes.pop(note_id, None) is not None


# Singleton instance for use by routers
note_storage = InMemoryNoteStorage()
