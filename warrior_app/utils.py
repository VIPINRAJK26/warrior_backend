from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

def generate_invoice_pdf(order, invoice_number):
    """Generate PDF for the given order with a tailored format."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    elements = []

    # Title
    elements.append(Paragraph("<b>Tax Invoice</b>", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Invoice Number: {invoice_number}", styleN))
    elements.append(Paragraph(f"Invoice Date: {order.created_at.date()}", styleN))
    elements.append(Spacer(1, 24))

    # Seller (Hardcoded) 
    seller = [
        "<b>SMART ENTERPRISES</b>",
        "11/505C, MULLAMPARA MANJERI",
        "MALAPPURAM, PIN: 676121",
        "GSTIN: 32ALSPY4534A1ZO",
        "State: Kerala, Code: 32"
    ]
    for s in seller:
        elements.append(Paragraph(s, styleN))
    elements.append(Spacer(1, 24))

    # Customer
    buyer = [
        "<b>Billed To</b>",
        order.customer_name,
        order.shipping_address,
        f"{order.city}, {order.state}, {order.zip_code}",
        f"phone: {order.customer_phone}",
        f"email: {order.customer_email}",
    ]
    for b in buyer:
        elements.append(Paragraph(b, styleN))
    elements.append(Spacer(1, 24))

    # Items table
    data = [['Sl', 'Description','Model No.', 'Qty', 'Unit Rate', 'Total']]
    for i, item in enumerate(order.items.all(), start=1):
        qty = item.quantity
        model=item.product.model_number
        rate = item.product.price
        total = qty * rate
        data.append([str(i), item.product.title, model, str(qty) ,f"{rate:.2f}", f"{total:.2f}"])
        
    

    table = Table(data, colWidths=[30, 200, 90, 50, 60, 60])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("18% GST is included in this total price.", styleN))
    elements.append(Spacer(1, 24))

    elements.append(Spacer(1, 24))
    elements.append(Paragraph("This is a computer generated Invoice.", styles['Italic']))
    elements.append(Paragraph("Original Invoice will be provided at the time of delivery.", styles['Italic']))

    doc.build(elements)

    buffer.seek(0)  # move back to start
    return buffer
