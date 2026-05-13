import unittest
import logging
from data_generator.generator_2 import EventGenerator, Event

class TestEventGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EventGenerator()
        self.logger = logging.getLogger("test_logger")
        self.logger.addHandler(logging.NullHandler())

    def test_generate_event(self):
        event = self.generator.generate_event(self.logger)
        self.assertIsNotNone(event)
        self.assertIsInstance(event, Event)
        self.assertTrue(event.event_id.startswith("event_"))

    def test_generate_events_batch(self):
        num_events = 5
        events = self.generator.generate_events(num_events, self.logger)
        self.assertEqual(len(events), num_events)
        for event in events:
            self.assertIsInstance(event, Event)

if __name__ == "__main__":
    unittest.main()
