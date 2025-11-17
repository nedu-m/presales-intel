from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Brief
from app.services.intelligence import IntelligenceService
from app.templates_config import templates

router = APIRouter(prefix="/briefs", tags=["briefs"])


@router.post("/generate", response_class=HTMLResponse)
async def generate_brief(
    request: Request,
    company_name: str = Form(...),
    attendees: str = Form(None),
    db: Session = Depends(get_db)
):
    """Generate intelligence brief for a meeting"""
    
    # Initialize intelligence service
    intel_service = IntelligenceService()
    
    try:
        # Generate brief sections
        brief_data = await intel_service.generate_brief(
            company_name=company_name,
            attendees=attendees
        )
        
        # Save to database
        brief = Brief(
            company_name=company_name,
            meeting_date=None,
            attendees=attendees,
            company_context=brief_data["company_context"],
            attendee_analysis=brief_data.get("attendee_analysis"),
            tech_stack=brief_data.get("tech_stack"),
            competitive_landscape=brief_data.get("competitive_landscape"),
            suggested_questions=brief_data.get("suggested_questions"),
            full_brief=brief_data["full_brief"]
        )
        db.add(brief)
        db.commit()
        db.refresh(brief)
        
        # Return the brief component
        return templates.TemplateResponse(
            "components/brief_result.html",
            {
                "request": request,
                "brief": brief,
                "brief_data": brief_data
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "components/error.html",
            {
                "request": request,
                "error": str(e)
            }
        )


@router.get("/history", response_class=HTMLResponse)
async def brief_history(
    request: Request,
    db: Session = Depends(get_db)
):
    """View previously generated briefs"""
    briefs = db.query(Brief).order_by(Brief.created_at.desc()).limit(20).all()
    
    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "briefs": briefs
        }
    )


@router.get("/{brief_id}", response_class=HTMLResponse)
async def view_brief(
    brief_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """View a specific brief"""
    brief = db.query(Brief).filter(Brief.id == brief_id).first()
    
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    
    return templates.TemplateResponse(
        "brief_detail.html",
        {
            "request": request,
            "brief": brief
        }
    )

