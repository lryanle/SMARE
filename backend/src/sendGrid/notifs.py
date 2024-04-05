import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..utilities import logger

logger = logger.SmareLogger()

# Set up SendGrid API key
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
sg = SendGridAPIClient(SENDGRID_API_KEY)

def send_daily_email_report(recipient_email, report_data):
    """
    Send a daily email report to the specified recipient email address.
    """
    message = Mail(
        from_email='tadero230@gmail.com',
        to_emails=recipient_email,
        subject='Daily Report',
        html_content='<p>Here is your daily report:</p>' + report_data
    )
    try:
        response = sg.send(message)
        logger.info('Notifs: Daily email report sent successfully')
    except Exception as e:
        if hasattr(e, 'status_code') and hasattr(e, 'body'):
            logger.debug(f'Failed to send daily email report: HTTP {e.status_code}, {e.body}')
        else:
            logger.debug(f'Failed to send daily email report: {e}')


def send_flagged_report_notification(recipient_email, report_id):
    """
    Send an email notification when a new report is flagged.
    """
    message = Mail(
        from_email='tadero230@gmail.com',
        to_emails=recipient_email,
        subject='New Flagged Report',
        html_content=f'<p>A new report with ID {report_id} has been flagged.</p>'
    )
    try:
        response = sg.send(message)
        logger.info('Notifs: Flagged report notification sent successfully')
    except Exception as e:
        if hasattr(e, 'status_code') and hasattr(e, 'body'):
            logger.debug(f'Failed to send flagged report notification: HTTP {e.status_code}, {e.body}')
        else:
            logger.debug(f'Failed to send flagged report notification: {e}')

