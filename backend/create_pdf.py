from fpdf import FPDF
import datetime, os, smtplib, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def create_pdf(email, optimized_irrigation, farm_id, money_info, energy_info, week_weather):
    print("IN PDF")
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 20)      
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, f"Plot {farm_id} Irrigation Optimization Plan", align="C", ln=True)

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
    for i, day in enumerate(week_weather):
        pdf.multi_cell(0, 5, f"- Day {i+1}: High - {day['max_temp_f']}f, Low - {day['min_temp_f']}f, Total Rain (mm) - {day['total_precip_mm']}, Humidity - {day['avg_humidity']}, Weather - {day['text']}")

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.cell(20, 10, "Cost and Energy Benefits: ")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.multi_cell(0, 5, f"This optimization plan will save you ${money_info['plot_money_saved']}. The previous amount of gallons used is {money_info['plot_irrigation_given_gallons']}, this approach asks for {money_info['plot_irrigation_optimized_gallons']} gallons of water")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.multi_cell(0, 5, f"This optimization plan will save the average Kansas farmer ${money_info['converted_money_saved']}. The previous amount of gallons used is {money_info['converted_irrigation_given_gallons']}, this approach asks for {money_info['converted_irrigation_optimized_gallons']} gallons of water")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(0, 10, f"This optimization plan will save you {energy_info['plot_optimized_energy']} killowat-hours in energy")

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(0, 10, f"This optimization plan will save the average Kansas farmer {energy_info['converted_optimized_energy']} killowat-hours in energy")

    # Specify the full path to the PDF file
    pdf_file_path = os.path.join(os.getcwd(), "Irrigation-Optimization.pdf")

    # Save the PDF to the specified path
    pdf.output(pdf_file_path)

    send_email(email, pdf_file_path)
    print("CREATED PDF: ", pdf_file_path)
    return pdf_file_path

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