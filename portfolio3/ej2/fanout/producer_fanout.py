
import pika, sys
c = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = c.channel()
ch.exchange_declare(exchange='logs', exchange_type='fanout')
msg = " ".join(sys.argv[1:])
ch.basic_publish(exchange='logs', routing_key='', body=msg)
print("Sent")
c.close()
