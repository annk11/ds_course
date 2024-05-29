import os
import glob
import smtplib
from datetime import datetime


def send_notification(email, txt):
    sender = 'ao.korta@yandex.ru'
    sender_password = 'Kkorta1994!'
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)

    for to_item in email:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            sender, to_item, f'[TEST REPORT {current_time}]')
        msg += txt
        mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()

def create_message(message):
    half_name = 'newman'
    files = glob.glob(os.path.join(report_path, f'*{half_name}*'))  # file name
    latest_file = max(files, key=os.path.getctime)  # fresh file
    report_file = open(latest_file, 'r', encoding='utf-8')
    html = report_file.read()
    message += html
    return message

# Path to Postman collection/environment
postman_collection = "C:/Users/URIST/est_collection.postman_collection.json"
postman_environment = "C:/Users/URIST/dev_stand_ml.postman_environment.json"

# Path to save report
report_path = "C:\\Users\\URIST"

# Current date for headline
current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

# Command text
cmd = f"newman run {postman_collection} -e {postman_environment} -r cli,html --reporter-html-export {report_path} --delay-request 4000"

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
        <p class="bold-green-text">Collection was completed. All tests passed successfully!</p>
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
            <p class="bold-red-text">Collection was completed. An error occurred while executing tests.</p>
        </body>
        </html>
        """
    message = create_message(html_text)
    send_notification({'nikia@omegafuture.ru'}, message)