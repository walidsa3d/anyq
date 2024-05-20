import json
from confluent_kafka import Producer                                                                                                                       
from confluent_kafka import Consumer                                                                                                                      

class KafkaQueue:

    def __init__(self, url=None):
        self.kafka_url = url
        self.group_id = "mygroupid"
        self.topic = "hello"
        self._init()                                                                                                  

    def _init(self):
        self.conf = {}       
        self.conf["bootstrap.servers"] = [self.kafka_url]
        self.producer = Producer(self.conf)
        self.conf["group.id"] = self.group_id
        self.consumer = Consumer(self.conf)
        #self.consumer.subscribe([self.topic])

    def put(self, msg):
        msg = json.dumps(msg)                                                                                                                              
        self.producer.produce(self.topic, value=msg)                                                                                                     
        self.producer.flush()

    def get(self):
        msg = self.consumer.poll(1.0)
        msg = json.loads(msg.value())
        return msg

    def qsize(self):
        pass

    def delete(self):
        pass