from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from config.database import contact_messages
from middleware.auth import require_role

router = APIRouter(tags=["Contact"])

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

@router.post("/contact")
async def send_contact_message(message: ContactMessage):
    """Handle contact form submissions"""
    try:
        # Store the message in database
        message_id = str(uuid.uuid4())
        message_doc = {
            "id": message_id,
            "name": message.name,
            "email": message.email,
            "phone": message.phone,
            "message": message.message,
            "status": "new",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await contact_messages.insert_one(message_doc)
        
        print(f"Contact message received from {message.name} ({message.email}):")
        print(f"Phone: {message.phone}")
        print(f"Message: {message.message}")
        print(f"Received at: {datetime.now(timezone.utc).isoformat()}")
        
        # You can add email sending logic here using services like:
        # - SendGrid
        # - Gmail SMTP
        # - AWS SES
        # etc.
        
        return {
            "message": "Contact message received successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process contact message")

@router.get("/contact/messages", response_model=List[dict])
async def get_contact_messages(current_user: dict = Depends(require_role("admin"))):
    """Get all contact messages (admin only)"""
    try:
        messages = await contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve contact messages")

@router.put("/contact/messages/{message_id}")
async def update_contact_message_status(message_id: str, status_data: dict, current_user: dict = Depends(require_role("admin"))):
    """Update contact message status (admin only)"""
    try:
        new_status = status_data.get("status")
        if new_status not in ["new", "read", "replied", "archived"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        await contact_messages.update_one(
            {"id": message_id},
            {"$set": {"status": new_status, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        updated_message = await contact_messages.find_one({"id": message_id}, {"_id": 0})
        return updated_message
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update message status")