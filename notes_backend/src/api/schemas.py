from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base schema for Note with only the content."""
    content: str = Field(..., description="The content of the note.")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a new Note (only content required)."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating a Note, all fields are optional."""
    content: Optional[str] = Field(None, description="The updated content of the note.")

# PUBLIC_INTERFACE
class Note(NoteBase):
    """Schema representing a Note, with an ID."""
    id: int = Field(..., description="Unique ID for the note.")
