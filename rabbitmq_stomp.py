import pika

mq_creds  = pika.PlainCredentials(
    username = "guest",
    password = "guest")

mq_params = pika.ConnectionParameters(
    host         = "localhost",
    credentials  = mq_creds,
    virtual_host = "/")


mq_routing_key = "test_hello"

mq_conn = pika.BlockingConnection(mq_params)

mq_chan = mq_conn.channel()
mq_chan.exchange_declare(exchange="test_exchange",
                                     exchange_type="topic",
                                     passive=False,
                                     durable=True,
                                     auto_delete=False)
mq_chan.queue_declare(queue=mq_routing_key, durable=True)
mq_chan.queue_bind(
            queue=mq_routing_key, exchange='test_exchange', routing_key=mq_routing_key)
mq_chan.basic_publish(
    exchange    = 'test_exchange',
    routing_key = mq_routing_key,
    body        = 'hello')
