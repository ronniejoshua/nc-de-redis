import json
import kafka
import redis
import sys
from pprint import pprint


# Kafka Configuration
BootstrapServers = ['localhost:9027']
TopicName = 'AppDataProcessed'
consumer = kafka.KafkaConsumer(TopicName, 
                                bootstrap_servers = BootstrapServers,
                                auto_offset_reset = 'latest',
                                enable_auto_commit=True,
                                auto_commit_interval_ms=1000,
                                group_id = 'AppDataProcessedRedis'
                                )


# Redis Configuration
redis_cxn = redis.Redis(
    host='localhost',
    port=6379, 
    db=0,
    password='Ronnie123!@#')

def get_record_from_redis(uuid_key):
    return redis_cxn.get(uuid_key)

def set_record_into_redis(redis_cxn, kafka_message):
    dd = json.loads(kafka_message.value)
    message_key = dd['value']['personal_data']['uuid']
    message_value = json.dumps(dd['value'], ensure_ascii=False)
    redis_cxn.set(message_key, message_value)
    pprint(json.loads(get_record_from_redis(message_key)))

if __name__ == "__main__":
    try:
        for message in consumer:
            print(message)
            set_record_into_redis(redis_cxn, message)
    except KeyboardInterrupt:
        sys.exit()


# Basic Redis Commands
    # docker-compose up -d
    # docker exec -it nc-de-redis sh
    # redis-cli -a Ronnie123!@#
    # get 452b9a46-606b-450a-a171-a5160307449a
    # flushall
    # docker-compose down

# docker-compose -f /home/ronniejoshua/superset/docker-compose-non-dev.yml up
