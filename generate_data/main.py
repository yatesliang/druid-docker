
# load files and print every line
import time
import threading

import pandas as pd
from kafka import KafkaProducer
from json import dumps
import datetime

producer = KafkaProducer(
    value_serializer=lambda m: dumps(m).encode('utf-8'),
    bootstrap_servers=['127.0.0.1:9092'])
time_pattern = "%m/%d/%Y %H:%M:%S %p"


def init_producer():
    global producer
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['127.0.0.1:9092'])


def get_time(time_str, interval):
    time.sleep(interval)
    return datetime.datetime.now().timestamp()
    # return datetime.datetime.strptime(time_str, time_pattern).timestamp()


def load(filename):
    return pd.read_csv(filename)


def load_by_schema(schema, interval=60, limit=None, offset=None):
    filename = schema.get("filename", None)
    topic = schema.get("topic", None)
    fields = schema.get("fields", None)
    if not filename or not topic or not fields:
        return
    df = load(filename)
    for index, row in df.iterrows():
        if offset is not None and index <= offset:
            continue
        if limit is not None and index > limit:
            break
        data = dict()
        for field in fields:
            if "Time" in field:
                data[field] = get_time(row[field], interval)
            else:
                data[field] = row[field]
        #
#        print(data)
        send_msg(topic=topic, data=data)


def send_msg(topic, data):
    a = producer.send(topic, data)
    # print(a.__dict__)
    producer.flush()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prefix_path = "../data/"
    step_schema = {"filename": "{}{}".format(prefix_path, "minuteStepsNarrow_merged.csv"),
                   "topic": "minute_level_step",
                   "fields": ["Id", "ReportTime", "Value"]}

    sleep_schema = {"filename": "{}{}".format(prefix_path, "minuteSleep_merged.csv"),
                    "topic": "minute_level_sleep",
                    "fields": ["Id", "ReportTime", "Value"]}

    calories_schema = {"filename": "{}{}".format(prefix_path, "minuteCaloriesNarrow_merged.csv"),
                       "topic": "minute_level_calories",
                       "fields": ["Id", "ReportTime", "Value"]}

    heartbeat_schema = {"filename": "{}{}".format(prefix_path, "heartrate_seconds_merged.csv"),
                        "topic": "second_level_heartbeat",
                        "fields": ["Id", "ReportTime", "Value"]}

    intensity_schema = {"filename": "{}{}".format(prefix_path, "minuteIntensitiesNarrow_merged.csv"),
                        "topic": "minute_level_intensity",
                        "fields": ["Id", "ReportTime", "Value"]}

    met_schema = {"filename": "{}{}".format(prefix_path, "minuteMETsNarrow_merged.csv"),
                  "topic": "minute_level_met",
                  "fields": ["Id", "ReportTime", "Value"]}

    weight_schema = {"filename": "{}{}".format(prefix_path, "weightLogInfo_merged.csv"),
                     "topic": "weight_report",
                     "fields": ["Id", "ReportTime", "WeightKg", "WeightPounds", "Fat", "BMI", "IsManualReport"]}

    threading.Thread(target=load_by_schema, args=(step_schema,)).start()
    threading.Thread(target=load_by_schema, args=(sleep_schema,)).start()
    threading.Thread(target=load_by_schema, args=(calories_schema,)).start()
    threading.Thread(target=load_by_schema, args=(heartbeat_schema,1,)).start()
    threading.Thread(target=load_by_schema, args=(intensity_schema,)).start()
    threading.Thread(target=load_by_schema, args=(met_schema,)).start()
    threading.Thread(target=load_by_schema, args=(weight_schema,)).start()
    # load_by_schema(step_schema)
    # load_by_schema(sleep_schema)
    # load_by_schema(calories_schema)
#    load_by_schema(heartbeat_schema,1)
    # load_by_schema(intensity_schema)
    # load_by_schema(met_schema)
    # load_by_schema(weight_schema)
    producer.close()
