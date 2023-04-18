import smtplib

email_server = "smtp-relay.sendinblue.com"
email_port = 587
email_username = "ourrestaurantproject2@gmail.com"
email_password = "8HEP46fKMNbQ32mJ"

try:
    with smtplib.SMTP(email_server, email_port) as server:
        server.starttls()  # Add this line to use TLS
        server.login(email_username, email_password)
        print("Successfully connected to the email server")
except Exception as e:
    print("Error connecting to the email server:", e)