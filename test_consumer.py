from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
   'minute_level_heartbeat',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['127.0.0.1:9092'])


# print(consumer)
for m in consumer:
    print(m.value)
