from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
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

@router.post("/export-pdf")
async def export_analysis_to_pdf(analysis_result: dict):
    """Export contract analysis to PDF report"""
    try:
        from app.utils.pdf_export import pdf_generator
        
        if pdf_generator is None:
            raise HTTPException(
                status_code=501,
                detail="PDF export not available. Install reportlab: pip install reportlab"
            )
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_contract_report(analysis_result)
        
        # Return PDF as response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=contract_analysis_{analysis_result.get('overall_risk_score', 0)}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
