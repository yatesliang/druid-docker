from kafka import KafkaProducer
from json import dumps
import time
producer = KafkaProducer(
   value_serializer=lambda m: dumps(m).encode('utf-8'), 
   bootstrap_servers=['127.0.0.1:9092'])

a = producer.send("minute_level_step", value={"Id": 1, "ReportTime": time.time(), "value": 10})
producer.close()
print(a.__dict__)
