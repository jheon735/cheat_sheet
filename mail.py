import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com', 587)  #gmail사용시
smtp.ehlo()  # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('id@gmail.com', 'password')

msg = MIMEText('내용')
msg['Subject'] = '제목'
msg['To'] = 'receiver@gmail.com'
smtp.sendmail('id@gmail.com', 'receiver@gmail.com', msg.as_string())

smtp.quit()