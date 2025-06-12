from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

def generate_invoice_pdf(order, invoice_number):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleB = styles['BodyText']
    styleH = styles['Heading2']

    elements = []

    # Title & Header Info
    elements.append(Paragraph("<b>Tax Invoice</b>", styleH))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"<b>Invoice No:</b> {invoice_number}", styleN))
    elements.append(Paragraph(f"<b>Date:</b> {order.created_at.strftime('%d-%b-%Y')}", styleN))
    elements.append(Spacer(1, 12))

    # Seller and Buyer Info
    seller_info = [
        "SMART ENTERPRISES",
        "11/505C, MULLAMPARA MANJERI",
        "MALAPPURAM, PIN:676121",
        "GSTIN/UIN: 32ALSPY4534A1ZO",
        "State Name: Kerala, Code: 32"
    ]
    buyer_info = [
        order.customer_name.upper(),
        f"{order.shipping_address}",
        f"{order.city}, {order.state}, {order.zip_code}",
        f"Phone: {order.customer_phone}",
        f"Email: {order.customer_email}"
    ]
    seller = [[Paragraph("<b>Seller (From)</b>", styleB)]] + [[Paragraph(x, styleN)] for x in seller_info]
    buyer = [[Paragraph("<b>Buyer (To)</b>", styleB)]] + [[Paragraph(x, styleN)] for x in buyer_info]

    table = Table([[Table(seller), Table(buyer)]], colWidths=[270, 270])
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Items Table
    data = [['Sl No.', 'Description of Goods', 'HSN/SAC', 'Quantity', 'Rate', 'per', 'Disc. %', 'Amount']]
    total = 0
    for i, item in enumerate(order.items.all(), start=1):
        qty = item.quantity
        price = item.product.price
        subtotal = qty * price
        total += subtotal
        data.append([
            str(i),
            item.product.title,
            "85044010",
            f"{qty:.3f} Pcs",
            f"{price:.2f}",
            "Pcs",
            "0",
            f"{subtotal:.2f}"
        ])

    # GST & Total
    cgst = total * 0.09
    grand_total = total + cgst
    data.append(["", "", "", "", "", "", "CGST 9%", f"{cgst:.2f}"])
    data.append(["", "", "", "", "", "", "<b>Total</b>", f"<b>{grand_total:.2f}</b>"])

    table = Table(data, colWidths=[35, 160, 65, 65, 65, 40, 55, 75])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("This is a Computer Generated Invoice", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
