from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import ContractAnalysisRequest, ContractAnalysisResponse
from app.agents.contract_agent import contract_agent
import pypdf

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: ContractAnalysisRequest):
    """Analyze contract for risks and compliance"""
    try:
        result = contract_agent.analyze(
            contract_text=request.contract_text,
            jurisdiction=request.jurisdiction
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-file", response_model=ContractAnalysisResponse)
async def analyze_contract_file(
    file: UploadFile = File(...),
    jurisdiction: str = "All-India"
):
    """Analyze contract from uploaded PDF/TXT file"""
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            import io
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file.filename.endswith('.txt'):
            text = content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Only PDF and TXT files supported")
        
        # Analyze
        result = contract_agent.analyze(
            contract_text=text,
            jurisdiction=jurisdiction
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
