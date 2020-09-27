from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from concurrent.futures import ThreadPoolExecutor

from appname.config import BaseConfig
from appname.log import logger


def send_email(receiver_list, subject, text_content=None, attachment=None, attachment_name=None):
    # 检查配置
    email_server = BaseConfig.EMAIL_SERVER
    sender_user = BaseConfig.SENDER_USER
    sender_token = BaseConfig.SENDER_TOKEN
    sender_name = BaseConfig.SENDER_NAME
    if email_server is None or sender_user is None or sender_token is None:
        logger.error("need email config")
        return {'send failed': "need email config"}

    # 基础
    sender_str = f"{sender_name} <{sender_user}>"
    mail = MIMEMultipart()
    mail['Subject'] = Header(subject, 'utf-8')
    mail['From'] = Header(sender_str, 'utf-8')
    mail['To'] = Header(','.join(receiver_list), 'utf-8')

    # 加正文
    if text_content:
        text = MIMEText(text_content, 'plain', 'utf-8')
        mail.attach(text)
    # 加附件
    if attachment is not None:
        if isinstance(attachment, BytesIO):
            att = MIMEText(attachment.read(), 'base64', 'utf-8')
        else:
            with open(attachment, 'rb') as f:
                att = MIMEText(f.read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f'attachment; filename="{attachment_name}"'
        mail.attach(att)

    # 发送
    try:
        with smtplib.SMTP_SSL(email_server, 465) as server:
            server.login(sender_user, sender_token)
            send_res = server.sendmail(sender_str, receiver_list, mail.as_string())
        return send_res
    except Exception as e:
        logger.error("email send failed with error: {}".format(e))
        return {'send failed': str(e)}


def async_send_email(receiver_list, subject, text_content=None, attachment=None, attachment_name=None):
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(send_email, receiver_list, subject, text_content, attachment, attachment_name)
