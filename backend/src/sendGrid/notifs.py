import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ..utilities import logger

logger = logger.SmareLogger()

# Set up SendGrid API key
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
sg = SendGridAPIClient(SENDGRID_API_KEY)

def format_listing_html(listing):
    """
    Format the HTML representation of a car listing.
    Highlight the listing in red if the risk score is above 50.
    """
    html = f"""
        <tr>
            <td>{listing['year']}</td>
            <td>{listing['make']}</td>
            <td>{listing['model']}</td>
            <td>{listing['price']}</td>
        </tr>
    """

    if listing.get('risk_score', 0) > 50:
        html = f'<tr style="background-color: #FFCCCC;">{html}</tr>'

    return html
def send_daily_email_report(recipient_emails, listings):
    """
    Send a daily email report to the specified recipient email addresses.
    Include only necessary data for each car listing.
    Highlight listings with risk scores above 50 in red.
    """
    # Try to convert listings to a list if it's not already
    if not isinstance(listings, list):
        try:
            listings = [listings]
        except Exception as e:
            logger.error(f'Failed to convert listings to a list: {e}')
            return

    # Format each listing as HTML
    formatted_listings = [format_listing_html(listing) for listing in listings]

    # Construct the HTML content for the email
    report_data = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 20px;
                }}
                .header {{
                    background-color: #FF5733;
                    color: white;
                    padding: 10px;
                    text-align: center;
                }}
                .description {{
                    margin-top: 20px;
                    margin-bottom: 20px;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                }}
                .listing-table {{
                    width: 100%;
                    border-collapse: collapse;
                    border: 1px solid #ddd;
                    margin-top: 20px;
                }}
                .listing-table th, .listing-table td {{
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                .listing-table th {{
                    background-color: #f2f2f2;
                }}
                .flagged-listing {{
                    background-color: #FFCCCC;
                }}
                .button {{
                    display: inline-block;
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 25px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Welcome to SMARE!</h1>
            </div>
            <div class="description">
                <p>Dear user,</p>
                <p>Welcome to SMARE (Smart Auto Risk Evaluation) - your trusted platform for evaluating auto risk.</p>
                <p>Our platform employs cutting-edge algorithms to analyze various data points of car listings, including historical data, market trends, and predictive analytics, to provide you with accurate risk assessments.</p>
                <p>Thank you for choosing SMARE for your auto risk evaluation needs!</p>
            </div>
            <div style="margin-top: 20px;">
                <h2>Here is your daily report:</h2>
                <table class="listing-table">
                    <tr>
                        <th>Year</th>
                        <th>Make</th>
                        <th>Model</th>
                        <th>Price</th>
                    </tr>
                    {''.join(formatted_listings)}
                </table>
            </div>
            <div style="margin-top: 20px;">
                <p>To subscribe or unsubscribe from our daily reports, click <a href="subscribe_link" class="subscribe">here</a>.</p>
            </div>
        </body>
        </html>
    """

    # Iterate over each recipient email and send the email separately
    for recipient_email in recipient_emails:
        # Create the email message
        message = Mail(
            from_email='smare.official@gmail.com',
            to_emails=recipient_email,
            subject='Daily Report from SMARE',
            html_content=report_data
        )

        try:
            # Send the email
            response = sg.send(message)
            logger.info(f'Notifs: Daily email report sent successfully to {recipient_email}')
        except Exception as e:
            if hasattr(e, 'status_code') and hasattr(e, 'body'):
                logger.debug(f'Failed to send daily email report to {recipient_email}: HTTP {e.status_code}, {e.body}')
            else:
                logger.debug(f'Failed to send daily email report to {recipient_email}: {e}')

def send_flagged_report_notification(recipient_emails, flagged_listing):
    """
    Send an email notification with detailed information about flagged listings.
    """
    # Check if flagged_listing is a dictionary
    if isinstance(flagged_listing, dict):
        # Extract relevant information from the flagged listing
        listing_id = flagged_listing.get('_id', '')
        year = flagged_listing.get('year', '')
        make = flagged_listing.get('make', '')
        model = flagged_listing.get('model', '')
        price = flagged_listing.get('price', '')
        
        # Construct email content
        html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f2f2f2;
                        padding: 20px;
                    }}
                    .header {{
                        background-color: #FF5733;
                        color: white;
                        padding: 10px;
                        text-align: center;
                    }}
                    .content {{
                        margin-top: 20px;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 5px;
                    }}
                    .warning {{
                        color: red;
                        font-weight: bold;
                    }}
                    .listing-details {{
                        margin-top: 20px;
                        margin-bottom: 20px;
                        padding: 10px;
                        background-color: #f9f9f9;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Flagged Listing Report</h1>
                </div>
                <div class="content">
                    <p class="warning">Warning: The following listing has been flagged as potentially fraudulent. Please exercise caution when dealing with this vehicle.</p>
                    <div class="listing-details">
                        <p><strong>ID:</strong> {listing_id}</p>
                        <p><strong>Year:</strong> {year}</p>
                        <p><strong>Make:</strong> {make}</p>
                        <p><strong>Model:</strong> {model}</p>
                        <p><strong>Price:</strong> ${price}</p>
                        <!-- Add any other relevant information here -->
                    </div>
                </div>
            </body>
            </html>
        """

        # Iterate over each recipient email and send the email separately
        for recipient_email in recipient_emails:
            # Create the email message
            message = Mail(
                from_email='smare.official@gmail.com',
                to_emails=recipient_email,
                subject='New Flagged Listing Report',
                html_content=html_content
            )

            try:
                # Send the email
                response = sg.send(message)
                logger.info(f'Notifs: Flagged report notification sent successfully to {recipient_email}')
            except Exception as e:
                if hasattr(e, 'status_code') and hasattr(e, 'body'):
                    logger.debug(f'Failed to send flagged report notification to {recipient_email}: HTTP {e.status_code}, {e.body}')
                else:
                    logger.debug(f'Failed to send flagged report notification to {recipient_email}: {e}')
    else:
        logger.debug('Flagged listing is not a dictionary')
