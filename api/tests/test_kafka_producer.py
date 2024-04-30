import unittest
from unittest.mock import Mock, patch
from api.services.kafka_producer.producer import KafkaProducerService

from confluent_kafka import KafkaError


class TestKafkaProducer(unittest.TestCase):

    @patch('api.services.kafka_producer.producer.Producer')
    def setUp(self, mock_producer):
        self.kafka_producer = KafkaProducerService()

        # We need to modify the side_effect to pass the error and message to the delivery_report method
        def side_effect(topic, key, value, callback):
            callback(None, Mock())

        self.kafka_producer.producer = Mock()
        self.kafka_producer.producer.produce.side_effect = side_effect

    def tearDown(self):
        self.kafka_producer.producer = None

    def test_send_message(self):
        topic = 'test_topic'
        message = {'test': 'test'}
        key = 'test_key'
        response = self.kafka_producer.send_message(topic, message, key)
        self.assertEqual(response, True)

    def test_send_message_with_error(self):
        topic = None
        message = {'test': 'test'}
        key = 'test_key'
        self.kafka_producer.producer.produce.side_effect = Exception("test error: Topic cannot be empty")
        response = self.kafka_producer.send_message(topic, message, key)
        self.assertEqual(response, False)

    def test_send_message_with_empty_key(self):
        topic = 'test_topic'
        message = {'test': 'test'}
        response = self.kafka_producer.send_message(topic, message)
        # Assert that the producer was called with a random UUID as key
        self.kafka_producer.producer.produce.assert_called_with(
            topic=topic,
            key=unittest.mock.ANY,
            value=unittest.mock.ANY,
            callback=unittest.mock.ANY
        )
