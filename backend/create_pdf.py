from fpdf import FPDF
import datetime, os, smtplib, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

pdf = FPDF()

def create_pdf(email, optimized_irrigation, plot_number, dollar_cost, other_variables=None):
    pdf_directory = os.getcwd()
    pdf.add_page()

    pdf.set_font("Arial", "B", 20)      
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, f"Plot {plot_number} Irrigation Optimization Plan", align="C", ln=True)

    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Created By: Ctrl + Alt + Elite", align="C", ln=True)

    start_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=7)

    pdf.cell(0, 10, f"Week: {start_date} - {end_date}", align="C", ln=True)
    
    pdf.line(0, 40, 210, 40)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(20, 10, "Irrigation Amount: ")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(0, 10, f"This week we reccomend you use {optimized_irrigation}mm of water")


    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(15)

    pdf.cell(20, 10, "Summary: ")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    text = f"To determine the optimal irrigation amount for this week, we utilized a combination of historical weather data, soil moisture levels, and crop water requirements. Our predictive analytics model analyzes patterns in temperature, humidity, and precipitation forecasts to estimate the expected water needs for your specific plot. By integrating these variables, we can accurately predict the irrigation amount necessary to maintain healthy crop growth while minimizing water waste. This week's recommendation of {optimized_irrigation}mm is tailored to ensure that your crops receive the precise amount of water they need based on the latest weather insights."
    pdf.multi_cell(0, 5, text, align="C")

    pdf.ln(5)
    pdf.cell(0, 10, "The weather conditions are:", ln=True)
    pdf.cell(0, 10, "- Day 1: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 2: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 3: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 4: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 5: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 6: 75 degrees, 20% change of rain, 2mm rain", ln=True)
    pdf.cell(0, 10, "- Day 7: 75 degrees, 20% change of rain, 2mm rain", ln=True)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.cell(20, 10, "Cost Breakdown: ")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(0, 10, f"The cost of irrigation this week is ${dollar_cost} based on the gallon price in Colby, Kansas at $1.05")

    pdf.output(os.path.join(pdf_directory, "Irrigation-Optimization.pdf"))
    thread = threading.Thread(target=send_email, args=(email, pdf_directory))
    thread.start()

    return pdf_directory

def send_email(recipient, pdf_directory):
    try:
        me = "ctrl.alt.elite.taps@gmail.com"

        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Irrigation Optimization Plan"
        msg['From'] = me
        msg['To'] = recipient

        # Create the body of the message (HTML Version)
        html = """\
        <html>
        <head></head>
        <body>
            <p>Hi!<br><br>
            Please see the irrigation optimization report below!<br><br>
            Best,<br>
            Crtl + Alt + Elite Team
            <br>
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(html, 'html')

        # Attach parts into message container.
        msg.attach(part1)   

        #Attach the PDF to the email
        with open(pdf_directory, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(pdf_directory))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_directory)}"'
            msg.attach(part)

        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login('ctrl.alt.elite.taps@gmail.com', 'acik plrm mnzf lybx')
        mail.sendmail(me, recipient, msg.as_string())
        mail.quit()
    except Exception as e:
        print("ERROR: ", str(e))
