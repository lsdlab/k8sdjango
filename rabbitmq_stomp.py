import pika

mq_creds  = pika.PlainCredentials(
    username = "guest",
    password = "guest")

mq_params = pika.ConnectionParameters(
    host         = "localhost",
    credentials  = mq_creds,
    virtual_host = "/")

mq_exchange    = "amq.topic"
mq_routing_key = "test"

mq_conn = pika.BlockingConnection(mq_params)

mq_chan = mq_conn.channel()


mq_chan.basic_publish(
    exchange    = mq_exchange,
    routing_key = mq_routing_key,
    body        = 'hello')
