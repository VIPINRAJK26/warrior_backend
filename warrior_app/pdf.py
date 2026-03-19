from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_warranty_pdf(registration):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    line_gap = 18

    def draw(label, value):
        nonlocal y
        p.drawString(40, y, f"{label}: {value}")
        y -= line_gap

    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y, "Warranty Registration Details")
    y -= 30

    p.setFont("Helvetica", 10)
    draw("Name", registration.name)
    draw("Email", registration.email)
    draw("Phone", registration.phone)
    draw("Address", registration.address)
    draw("State", registration.state)
    draw("District", registration.district)
    draw("PIN Code", registration.pin_code)
    draw("Dealer", registration.dealer)
    draw("Product Type", registration.product_type)
    draw("Model Number", registration.model_number)
    draw("Serial Number", registration.serial_number)
    draw("Purchase Date", registration.purchase_date)
    draw("Warranty Period (Months)", registration.warranty_period_months)
    draw("Warranty End Date", registration.warranty_end_date)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
