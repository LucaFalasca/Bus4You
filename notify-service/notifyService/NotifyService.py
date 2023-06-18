import json
import os
import pickle
# for encoding/decoding messages in base64
from base64 import urlsafe_b64encode
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from mimetypes import guess_type as guess_mime_type

import pika
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
# Gmail API utils
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
our_email = 'bus4you-notification@bus4you-389820.iam.gserviceaccount.com'
OBJECT = 'Bus4You Notification - Il tuo itinerario è pronto!'
BODY = "%s Il tuo itinerario è pronto! Puoi visualizzarlo nella sezione MyRoutes dell'app Bus4You, puoi scegliere " \
       "se confermarlo o meno entro il %s alle %s.\n" \
       "Riepilogo prenotazione:\n\n" \
       "-Partenza: %s\n" \
       "-Arrivo: %s\n" \
       "-Distanza: %s Km\n" \
       "-Costo: %s €"


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("notifyService/credentials/token.pickle"):
        with open("notifyService/credentials/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("notifyService/credentials/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("notifyService/credentials/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


def build_message(destination, obj, body, attachments=[]):
    if not attachments:  # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, obj, body, attachments)
    ).execute()


def prepared_routes_callback(ch, method, properties, body):
    print("Received prepared routes message: " + body.decode('utf-8'))
    for itinerario in json.loads(body):
        scadenza = itinerario['route_expiration']
        mail_utente = itinerario['mail']
        costo = itinerario['it_cost']
        distanza = itinerario['it_distance']
        dt_partenza = itinerario['it_departure_time']
        dt_arrivo = itinerario['it_arrival_time']
        fermata_partenza = itinerario['it_departure_stop']
        fermata_arrivo = itinerario['it_arrival_stop']
        message = BODY % (mail_utente.split('@')[0], scadenza[0:10], scadenza[11:16],
                          dt_partenza[0:10] + ' ' + dt_partenza[11::16] + ' ' + fermata_partenza,
                          dt_arrivo[0:10] + ' ' + dt_arrivo[11::16] + ' ' + fermata_arrivo, distanza, costo)
        send_message(gmail_authenticate(), mail_utente, OBJECT, message, [])


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq'))
    channel = connection.channel()
    # Create a queue, if already exist nothing happens
    channel.queue_declare(queue='preparedRoutes1', durable=True)
    channel.basic_consume(queue='preparedRoutes1',
                          auto_ack=True,
                          on_message_callback=prepared_routes_callback)
    channel.start_consuming()
