from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def create_pdf(self, cause_list_data, metadata):
        """Generate PDF from cause list data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cause_list_{metadata['state']}_{metadata['district']}_{timestamp}.pdf"
        filepath = os.path.join("downloads", filename)
        
        # Create downloads directory if it doesn't exist
        os.makedirs("downloads", exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        title = f"Cause List - {metadata['type'].title()}"
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Court Information
        court_info = f"""
        <b>State:</b> {metadata['state']}<br/>
        <b>District:</b> {metadata['district']}<br/>
        <b>Court Complex:</b> {metadata['complex']}<br/>
        <b>Court:</b> {metadata['court']}<br/>
        <b>Date:</b> {metadata['date']}<br/>
        <b>Generated on:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        story.append(Paragraph(court_info, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Cause List Table
        if cause_list_data:
            # Table headers
            headers = ['Sr. No.', 'Case No.', 'Petitioner', 'Respondent', 'Purpose']
            table_data = [headers]
            
            # Table rows
            for case in cause_list_data:
                row = [
                    case.get('sr_no', ''),
                    case.get('case_no', ''),
                    case.get('petitioner', ''),
                    case.get('respondent', ''),
                    case.get('purpose', '')
                ]
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[0.8*inch, 1.5*inch, 2*inch, 2*inch, 1.5*inch])
            
            # Table styling
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("No cause list data found for the specified criteria.", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filepath
