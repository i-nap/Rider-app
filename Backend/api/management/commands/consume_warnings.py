from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json

class Command(BaseCommand):
    help = 'Consume rider warning events from Kafka'

    def handle(self, *args, **kwargs):
        consumer = KafkaConsumer(
            'rider-warnings',
            bootstrap_servers='localhost:9092',
            group_id='warning-consumer-group',
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            event = message.value
            print("⚠️ Received Warning:", event)
            # TODO: Save to DB or notify riders
