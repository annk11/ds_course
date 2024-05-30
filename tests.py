import os
import glob
import json
import base64
import smtplib
from datetime import datetime
import matplotlib.pyplot as plt


def send_notification(email, txt):
    sender = 'ao.korta@yandex.ru'
    sender_password = 'Kkorta1994!'
    mail_server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_server.login(sender, sender_password)

    for to_item in email:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            sender, to_item, f'TEST REPORT {current_time}')
        msg += txt
        mail_server.sendmail(sender, to_item, msg.encode('utf8'))
    mail_server.quit()

def create_message(message):
    half_name = 'newman'
    html_file = glob.glob(os.path.join(report_path, f'*{half_name}*.html'))  # html file name
    latest_html_file = max(html_file, key=os.path.getctime)  # fresh html file
    report_file = open(latest_html_file, 'r', encoding='utf-8')
    html = report_file.read()
    json_file = glob.glob(os.path.join(report_path, f'*{half_name}*.json'))  # json file name
    latest_json_file = max(json_file, key=os.path.getctime)  # fresh json file

    # Parsing json and create chart
    with open(latest_json_file, 'r') as file:
        data = json.load(file)
    total = data["run"]["stats"]["assertions"]["total"]
    failed = data["run"]["stats"]["assertions"]["failed"]
    labels = ["total", "failed"]
    values = [total, failed]
    colors = ['#60c464', '#ff7575']
    plt.bar(labels, values, color=colors, alpha=0.6)
    plt.xlabel("Assertions", fontsize=10, fontweight='bold')
    plt.ylabel("Count", fontsize=10, fontweight='bold')
    plt.title(f"Test results\n Total tests: {total}, Failed tests: {failed}")
    plt.savefig('C:/Users/URIST/result_chart.png')

    # Read attachment file
    with open('C:/Users/URIST/result_chart.png', 'rb') as file:
        attachment_file = file.read()

    # Message generation
    message += "<img src='data:image/png;base64," + base64.b64encode(attachment_file).decode('utf-8') + "'>"
    message += html
    return message

# Path to Postman collection/environment
postman_collection = "C:/Users/URIST/ests.postman_collection.json"
postman_environment = "C:/Users/URIST/dev_stand_ml.postman_environment.json"

# Path to save report
report_path = "C:/Users/URIST"

# Current date for headline
current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

# Command text
cmd = f"newman run {postman_collection} -e {postman_environment} -r cli,html,json --reporter-html-export " \
      f"{report_path} --reporter-json-export {report_path} --delay-request 4000"

process = os.system(cmd)

if process == 0:
    html_text = """\
        <html>
    <head>
        <style>
            .bold-green-text {
                font-weight: bold;
                font-size: 16px;
                color: ForestGreen;
            }
        </style>
    </head>
    <body>
        <p class="bold-green-text">Collections run completed. All tests passed successfully!</p>
    </body>
    </html>
    """
    message = create_message(html_text)
    send_notification({'nikia@omegafuture.ru'}, message)
else:
    html_text = """\
            <html>
        <head>
            <style>
                .bold-red-text {
                    font-weight: bold;
                    font-size: 16px;
                    color: Crimson;
                }
            </style>
        </head>
        <body>
            <p class="bold-red-text">Collections run completed. An error occurred while executing tests.</p>
        </body>
        </html>
        """
    message = create_message(html_text)
    send_notification({'nikia@omegafuture.ru'}, message)