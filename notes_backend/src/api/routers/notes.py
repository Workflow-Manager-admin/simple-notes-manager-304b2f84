from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from ..schemas import Note, NoteCreate, NoteUpdate
from ..storage import note_storage

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    responses={404: {"description": "Not found"}},
)

# PUBLIC_INTERFACE
@router.get("/", response_model=List[Note], summary="List all notes", description="Get a list of all notes.")
def list_notes():
    """
    Retrieve the complete list of notes.

    Returns:
        List of notes, each including its id and content.
    """
    return note_storage.list_notes()

# PUBLIC_INTERFACE
@router.post(
    "/", 
    response_model=Note, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note and return the note including its unique ID.",
)
def create_note(note_create: NoteCreate):
    """
    Create a new note.

    Parameters:
        note_create: The note to be created (content required).

    Returns:
        The created note object, including its ID.
    """
    return note_storage.create_note(content=note_create.content)

# PUBLIC_INTERFACE
@router.get(
    "/{note_id}", 
    response_model=Note,
    summary="Retrieve a note by ID",
    description="Get a single note by its unique ID.",
)
def get_note(note_id: int = Path(..., description="The unique ID of the note.")):
    """
    Get a specific note by ID.

    Parameters:
        note_id: ID of the note to retrieve.

    Returns:
        The corresponding note object if found.

    Raises:
        404 Not Found if the note doesn't exist.
    """
    note = note_storage.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    return note

# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=Note,
    summary="Update an existing note",
    description="Update the content of an existing note by its ID."
)
def update_note(note_id: int = Path(..., description="The unique ID of the note."),
                note_update: NoteUpdate = ...):
    """
    Update the content of a note.

    Parameters:
        note_id: ID of the note to update.
        note_update: The new data for the note; may contain content.

    Returns:
        The updated note object.

    Raises:
        404 Not Found if the note doesn't exist.
    """
    note = note_storage.update_note(note_id, content=note_update.content)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    return note

# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID. Returns 204 No Content if deletion is successful."
)
def delete_note(note_id: int = Path(..., description="The unique ID of the note.")):
    """
    Delete a note by ID.

    Parameters:
        note_id: ID of the note to delete.

    Returns:
        None if successful.

    Raises:
        404 Not Found if the note doesn't exist.
    """
    success = note_storage.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
