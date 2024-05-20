import pika 
import os
import json 
import pika.exceptions
from typing import Any 

class RabbitQueue:

    def __init__(self, 
                 qname=None,
                 host=None, 
                 port=None,
                 username="guest",
                 password="guest"
                 ):
        self.ampq_url = f"amqp://{username}:{password}@{host}:{port}"
        self.params = pika.URLParameters(self.ampq_url)
        self.params.socket_timeout = 5
        self.routing_key = ""
        self.qname = qname
        self._init(qname)

    def _init(self, queue_name:str):
        """Connect to server and declare queue.

        Args:
            queue_name (str): name of the queue
        """
        self.qname = queue_name
        try:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(self.qname)
        except pika.exceptions.ChannelClosed:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
            self.channel = self.connection.channel()

    def put(self, msg:Any):
        """Put message in a queue.

        Args:
            msg (Any): json-serializable message.
        """
        msg = json.dumps(msg)
        try:
            self.channel.basic_publish("", self.qname, msg)
            return True
        except Exception as e:
            print(e)
        return False 

    def get(self, ack=False)->Any:
        """Get message from the queue.

        Args:
            ack (bool, optional): acknowledge. Defaults to False.

        Returns:
            Any: message.
        """
        method_frame, header_frame, body = self.channel.basic_get(self.qname, not ack)
        if ack:
            self.channel.basic_ack(method_frame.delivery_tag)
        return json.loads(body)

    def delete(self):
        """Delete queue.

        Returns:
            bool: True or False.
        """
        return self.channel.queue_delete(queue=self.qname)
    
    def qsize(self)->int:
        """Get queue size.

        Returns:
            int: size of the queue.
        """
        ret = self.channel.queue_declare(self.qname, passive=True)
        return ret.method.message_count
