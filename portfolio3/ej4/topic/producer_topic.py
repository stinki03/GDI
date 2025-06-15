
import pika, sys
c = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = c.channel()
ch.exchange_declare(exchange='logs', exchange_type='topic')
key = sys.argv[1]
msg = " ".join(sys.argv[2:])
ch.basic_publish(exchange='logs', routing_key=key, body=msg)
print("Sent")
c.close()
