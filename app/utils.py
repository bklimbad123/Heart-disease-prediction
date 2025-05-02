import os
import tempfile
import pdfkit
from flask import render_template, current_app
from flask_mail import Message
from app import mail
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


def generate_pdf(report):
    """Generate a PDF report from a Report object"""
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        html_content = render_template('pdf_template.html', report=report)
        f.write(html_content.encode('utf-8'))
        temp_html = f.name

    # Generate PDF from HTML
    try:
        pdf = pdfkit.from_file(temp_html, False)
    except Exception as e:
        # If pdfkit fails, create a simple PDF with reportlab
        pdf = create_simple_pdf(report)
    finally:
        # Clean up temporary file
        os.unlink(temp_html)

    return pdf


def create_simple_pdf(report):
    """Create a simple PDF report using reportlab if pdfkit fails"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create content
    content = []

    # Title
    content.append(Paragraph(f"Heart Disease Prediction Report", styles['Title']))
    content.append(Spacer(1, 12))

    # Date
    content.append(Paragraph(f"Date: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Prediction result
    result_text = "Heart Disease Risk" if report.prediction else "No Heart Disease Risk"
    confidence = f"{report.confidence * 100:.2f}%"
    content.append(Paragraph(f"Prediction: {result_text}", styles['Heading2']))
    content.append(Paragraph(f"Confidence: {confidence}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Patient data
    content.append(Paragraph("Patient Data:", styles['Heading2']))

    # Create table data
    feature_names = report.get_feature_names()
    table_data = [["Feature", "Value"]]

    for key, name in feature_names.items():
        value = getattr(report, key)
        # Format gender
        if key == 'gender':
            value = 'Male' if value == 1 else 'Female'
        table_data.append([name, str(value)])

    # Create table
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    content.append(table)

    # Build PDF
    doc.build(content)
    pdf = buffer.getvalue()
    buffer.close()

    return pdf


def send_email_report(report, recipient_email):
    """Send a report via email"""
    subject = "Your Heart Disease Prediction Report"

    # Generate PDF attachment
    pdf_data = generate_pdf(report)

    # Create message
    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        body=f"Please find attached your heart disease prediction report from {report.timestamp.strftime('%Y-%m-%d')}."
    )

    # Attach PDF
    msg.attach(
        filename=f"heart_report_{report.id}.pdf",
        content_type="application/pdf",
        data=pdf_data
    )

    # Send email
    mail.send(msg)

    return True


def generate_chart_image(report, previous_reports=None):
    """Generate a chart image for visualization"""
    plt.figure(figsize=(10, 6))

    # Get numeric features for comparison
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    feature_names = report.get_feature_names()

    # Current report values
    current_values = [getattr(report, feature) for feature in numeric_features]

    # Previous reports average (if available)
    if previous_reports:
        prev_values = []
        for feature in numeric_features:
            values = [getattr(r, feature) for r in previous_reports if r.id != report.id]
            prev_values.append(sum(values) / len(values) if values else 0)

        # Plot previous values
        plt.plot(
            [feature_names[feature] for feature in numeric_features],
            prev_values,
            'o-',
            label='Previous Average'
        )

    # Plot current values
    plt.plot(
        [feature_names[feature] for feature in numeric_features],
        current_values,
        'o-',
        label='Current Report'
    )

    plt.title('Heart Health Metrics Comparison')
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save to BytesIO
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    # Encode as base64 for HTML embedding
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_data}"