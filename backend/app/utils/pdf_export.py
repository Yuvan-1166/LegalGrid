"""
PDF Export Utility
Generates professional PDF reports for contract analysis
"""

from typing import Dict, List
from datetime import datetime
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFReportGenerator:
    """Generate PDF reports for contract analysis"""
    
    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            spaceBefore=20
        ))
        
        # Risk score style
        self.styles.add(ParagraphStyle(
            name='RiskScore',
            parent=self.styles['Normal'],
            fontSize=36,
            textColor=colors.HexColor('#DC2626'),
            alignment=TA_CENTER,
            spaceAfter=10
        ))
    
    def _get_risk_color(self, score: int):
        """Get color based on risk score"""
        if score > 70:
            return colors.HexColor('#DC2626')  # Red
        elif score > 40:
            return colors.HexColor('#F59E0B')  # Yellow
        return colors.HexColor('#10B981')  # Green
    
    def generate_contract_report(self, analysis_result: Dict) -> bytes:
        """
        Generate PDF report for contract analysis
        
        Args:
            analysis_result: Contract analysis result dictionary
            
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Title
        elements.append(Paragraph("Contract Analysis Report", self.styles['CustomTitle']))
        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['CustomSubtitle']
        ))
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        elements.append(Paragraph(analysis_result.get('summary', 'No summary available'), 
                                self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Overall Risk Score
        risk_score = analysis_result.get('overall_risk_score', 0)
        risk_color = self._get_risk_color(risk_score)
        
        elements.append(Paragraph("Overall Risk Assessment", self.styles['SectionHeading']))
        
        # Risk score table
        risk_data = [
            ['Risk Score', 'Risk Level', 'Status'],
            [
                f"{risk_score}/100",
                'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 40 else 'LOW',
                '⚠️ Attention Required' if risk_score > 40 else '✓ Acceptable'
            ]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (0, 1), risk_color),
            ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, 1), 14),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Detailed Clause Analysis
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Clause Analysis", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        clauses = analysis_result.get('clauses', [])
        for i, clause in enumerate(clauses, 1):
            # Clause header
            elements.append(Paragraph(f"Clause {i}", self.styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Clause text
            elements.append(Paragraph(f"<b>Text:</b> {clause.get('clause', 'N/A')}", 
                                    self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Risk score
            clause_risk = clause.get('risk_score', 0)
            elements.append(Paragraph(
                f"<b>Risk Score:</b> <font color='{self._get_risk_color(clause_risk).hexval()}'>{clause_risk}/100</font>",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            # Red flags
            red_flags = clause.get('red_flags', [])
            if red_flags:
                elements.append(Paragraph("<b>⚠️ Red Flags:</b>", self.styles['Normal']))
                for flag in red_flags:
                    elements.append(Paragraph(f"• {flag}", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
            
            # Recommendations
            recommendations = clause.get('recommendations', [])
            if recommendations:
                elements.append(Paragraph("<b>✓ Recommendations:</b>", self.styles['Normal']))
                for rec in recommendations:
                    elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
            
            elements.append(Spacer(1, 0.2*inch))
            
            # Add page break after every 2 clauses
            if i % 2 == 0 and i < len(clauses):
                elements.append(PageBreak())
        
        # Footer
        elements.append(PageBreak())
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(
            "This report was generated by LegalGrid Smart Legal System",
            self.styles['CustomSubtitle']
        ))
        elements.append(Paragraph(
            "© 2026 LegalGrid. All rights reserved.",
            self.styles['CustomSubtitle']
        ))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes

# Global instance
pdf_generator = PDFReportGenerator() if REPORTLAB_AVAILABLE else None
