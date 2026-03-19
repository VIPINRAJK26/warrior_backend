from django.core.mail import EmailMessage
from django.conf import settings
from .pdf import generate_warranty_pdf

def send_admin_warranty_email(registration):
    pdf_buffer = generate_warranty_pdf(registration)

    subject = "New Warranty Registration"
    body = f"""
A new warranty has been registered.

Name: {registration.name}
Email: {registration.email}
Phone: {registration.phone}
Model: {registration.model_number}
Serial: {registration.serial_number}
Warranty End Date: {registration.warranty_end_date}
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.ADMIN_EMAIL,
    )

    email.attach(
        f"warranty_{registration.id}.pdf",
        pdf_buffer.read(),
        "application/pdf"
    )

    email.send(fail_silently=False)





def send_user_warranty_email(registration):
    subject = "Warranty Registration Confirmed ✅"

    body = f"""
Dear {registration.name},

Your product warranty has been successfully registered.

Here are your registration details:

Customer Name: {registration.name}
Email: {registration.email}
Phone: {registration.phone}

Product Type: {registration.product_type}
Model Number: {registration.model_number}
Serial Number: {registration.serial_number}

Purchase Date: {registration.purchase_date}
Warranty Period: {registration.warranty_period_months} months
Warranty Valid Until: {registration.warranty_end_date}

Dealer: {registration.dealer}
Registered On: {registration.created_at.date()}

Please keep this email for your records.

If you need any support, feel free to contact our service team.

Regards,
Warranty Support Team
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[registration.email],  # ✅ USER EMAIL
    )

    email.send(fail_silently=False)
