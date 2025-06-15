
import pika, sys
c = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = c.channel()
ch.exchange_declare(exchange='logs', exchange_type='direct')
s = sys.argv[1:]
q = ch.queue_declare(queue='', exclusive=True)
qname = q.method.queue
for i in s:
 ch.queue_bind(exchange='logs', queue=qname, routing_key=i)
def cb(ch, method, properties, body): print(f"Received: {body}")
ch.basic_consume(queue=qname, on_message_callback=cb, auto_ack=True)
ch.start_consuming()
