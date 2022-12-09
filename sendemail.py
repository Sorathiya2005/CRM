from matplotlib.pyplot import text
import content
import datetime
import smtplib
import ssl
from email.message import EmailMessage

class DailyMail():

    def __init__(self):
        self.content = {'quote': {'include': True, 'content': content.get_quotes()},
                        'weather': {'include': True, 'content': content.get_weather_forecast()},
                        'twitter': {'include': True, 'content': content.get_twitter_trends()},
                        'wikipedia': {'include': True, 'content': content.get_article()},
                        # 'News' : {'include' : True, 'content' : content.get_regular_news()}
                        }
        
        self.recipients_list = ['jaymahakal@gmail.com'] # receiver's email address
        self.sender_credentials = {'email': 'pythonhackers10@gmail.com', # your sender email address
                                   'password': ' '} # your sender password

        
    def send_email(self):
         # build email message
        msg = EmailMessage()
        msg['Subject'] = f'Daily Brief - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipients_list)

        # add Plaintext and HTML content
        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype='html')

        # secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)

    def format_message(self):
    ### Generating Plain Text ###
        text = f'<-- Your work - {datetime.date.today().strftime("%d %b %Y")} -->\n\n'

        # format news
        # if self.content['news']['include'] and self.content['news']['content']:
        #     text += f'<- News Updates in India->\n\n'
        #     for news in self.content['twitter']['content'][1:11]: # top ten
        #         text += f'{trend["name"]}\n'
        #     text += '\n'

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '<- motivational quotes ->\n\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["Author"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'<- Forecast for {self.content["weather"]["content"]["City"]}, {self.content["weather"]["content"]["Country"]} ->\n\n'
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format Twitter trends
        if self.content['twitter']['include'] and self.content['twitter']['content']:
            text += '<- Top Ten Twitter Trends ->\n\n'
            for trend in self.content['twitter']['content'][1:11]: # top ten
                text += f'{trend["name"]}\n'
            text += '\n'

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '<- Daily Random Learning ->\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'

 ### Generating HTML ###
         
        html = f"""<html>
    <body>
    <center>
        <h1>Daily Brief - {datetime.date.today().strftime('%d %B %Y')}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['Author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['City']}, {self.content['weather']['content']['Country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """               

            html += """
            </table>
                    """

        # format Twitter trends
        if self.content['twitter']['include'] and self.content['twitter']['content']:
            html += """
        <h2>Top Ten Twitter Trends</h2>
        <h5>Click on the trends to view more..</h5>
                    """

            for trend in self.content['twitter']['content'][0:10]: # top ten
                html += f"""
        <b><a href="{trend['url']}">{trend['name']}</a></b><p>
                        """

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h5>Click on the heading to view more..</h5>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}

if __name__ == '__main__':
    email = DailyMail()
    ##### test format_message() #####
    print("\nTesting email body generation...")
    message = email.format_message()

    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])

      ##### test send_email() #####
    print('\nSending test email...')
    email.send_email()