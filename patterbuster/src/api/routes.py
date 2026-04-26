from fastapi import APIRouter
from pydantic import BaseModel
import logging
from datetime import datetime

from src.db.tinydb_client import searches_table
from src.nlp.normalizer import normalize_text
from src.core.analyzer import analyze_prompt

router = APIRouter()

logger = logging.getLogger(__name__)

# defines modelo
class PromptRequest(BaseModel):
    prompt: str

@router.get("/searches")
def get_searches():
    return [
        {
            "id": str(doc.doc_id),
            **doc
        }
        for doc in searches_table.all()
    ]

class DocumentRequest(BaseModel):
    content: str

@router.post("/analyze/document")
def analyze(request: DocumentRequest):
    normalized = normalize_text(request.content)
    result = analyze_prompt(normalized)

    search = {
        "query": normalized,
        "result": {
            "riskScore": result.get("riskScore"),
            "findings": result.get("findings", [])
        },
        "createdAt": datetime.utcnow().isoformat()
    }

    #doc_id = searches_table.insert(search)

    #search["id"] = str(doc_id)
    search["id"] = 1
    return search