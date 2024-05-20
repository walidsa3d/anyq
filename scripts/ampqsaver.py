import pika 
import os 
import time
import psycopg2
import psycopg2.extras


class AMPQSaver:
   
    def __init__(self):
        self.queue = ""
        self.table = ""
        self.db_params = {
          "user":"postgres",
          "password": "postgres",
          "host": "127.0.0.1",
          "port": "5432",
          "database": "postgres_db"
        }

    def get_db_connection(self):
        con = psycopg2.connect(user="postgres",
                                 password="postgres",
                                 host="127.0.0.1",
                                 port="5432",
                                 database="postgres_db")
        return None
    
    def get_queue_connection(self):
      url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
      params = pika.URLParameters(url)
      connection = pika.BlockingConnection(params)

    def process(self, data):
      try:
        connection = self.db_connect()
        cursor = connection.cursor()
        keys = data[0].keys()
        insert_query = f"INSERT INTO {self.table} ({*keys}) VALUES %s"
        values = [(d['name'], d['age']) for d in data]
        psycopg2.extras.execute_values(cursor, insert_query, values)
        connection.commit()
        record = cursor.fetchone()
        record = cursor.fetchall()
        count = cursor.rowcount
        connection.commit()
        count = cursor.rowcount
      except Exception as e:
        pass
      finally:
        if (connection):
            cursor.close()
            connection.close()

    def process_function(self, msg):
      connection = self.get_queue_connection()
      channel = connection.channel() # start a channel
      channel.queue_declare(queue='scraper1') # Declare a queue

      
    def callback(self, ch, method, properties, body):
      process_function(body)
      channel.basic_consume('process',
        callback,
        auto_ack=True)
      channel.start_consuming()
      connection.close()
