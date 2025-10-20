from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def create_pdf(self, cause_list_data, metadata):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cause_list_{metadata.get('state','XX')}_{metadata.get('district','YY')}_{timestamp}.pdf"
        os.makedirs("downloads", exist_ok=True)
        filepath = os.path.join("downloads", filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        title_style = ParagraphStyle('Title', parent=self.styles['Heading1'], alignment=1, fontSize=14)
        story.append(Paragraph(f"Cause List - {metadata.get('type','')}", title_style))
        story.append(Spacer(1, 12))
        info = f"<b>State:</b> {metadata.get('state','')} &nbsp;&nbsp; <b>District:</b> {metadata.get('district','')} &nbsp;&nbsp; <b>Date:</b> {metadata.get('date','')}"
        story.append(Paragraph(info, self.styles['Normal']))
        story.append(Spacer(1, 12))
        if cause_list_data:
            headers = ['Sr. No.', 'Case No.', 'Petitioner', 'Respondent', 'Purpose']
            table_data = [headers]
            for c in cause_list_data:
                table_data.append([c.get('sr_no',''), c.get('case_no',''), c.get('petitioner',''), c.get('respondent',''), c.get('purpose','')])
            table = Table(table_data, colWidths=[0.7*inch,1.6*inch,2*inch,2*inch,1.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.grey),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                ('GRID',(0,0),(-1,-1),0.5,colors.black),
                ('FONTSIZE',(0,0),(-1,-1),8)
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No case data found.", self.styles['Normal']))
        doc.build(story)
        return filepath
