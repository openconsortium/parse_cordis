from parse_cordis import listing
from parse_cordis import project_xml
import pika
import sys
import json

def rabbit_mq_add(data, host='localhost', queue='cordis'):
	# Connect to RabbitMQ
	credentials = pika.PlainCredentials('guest', 'guest')
	parameters = pika.ConnectionParameters(
		host,
		5672,
		'/',
		credentials
	)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_declare(queue=queue, passive=False, durable=True)

	for el in data:
		p = project_xml.parse(el)
		p_json = json.dumps(p)

		# Add this to rabbitmq
		channel.basic_publish(exchange='',
                      routing_key='cordis',
                      body=p_json)
		
		print " [x] Sent cordis project with RCN " + str(el)

def rabbit_mq_from_cordis(limit, host, queue):
	l = listing.parseNew(limit)
	print "Parsed Cordis for last " + str(limit) + " entries"
	rabbit_mq_add(l, host, queue)


def rabbit_mq_from_json(json_file, host, queue):
	json_data = open(json_file)
	data = json.load(json_data)
	print "Read file " + json_file + ": " + str(len(data)) + " entries"
	rabbit_mq_add(data, host, queue)