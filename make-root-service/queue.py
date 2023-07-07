import pika
import json

MAKE_ROUTE_STOP_DATA_QUEUE_1 = 'make_route_stop_data_1'
PROPOSE_ROUTE_QUEUE = 'propose_route'

'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer in quanto un messaggio
può essere consumato una sola volta, sulla quale poi si pubblicheranno gli stessi messaggi'''
def init_rabbit_mq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitMq'))
    channel = connection.channel()
    channel.queue_declare(queue=PROPOSE_ROUTE_QUEUE, durable=True)
    return channel

def publish_message_on_queue(message, queue, channel):
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message.encode('utf-8'),
                          properties=pika.BasicProperties(delivery_mode=2))
    message_json = json.loads(message)
    print("Sent message\n" + json.dumps(message_json, indent = 2) + "\non queue: [" + queue + "]")