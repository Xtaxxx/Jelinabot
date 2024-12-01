# test_support_assistant.py
import unittest
from support_assistant import SupportAssistant
from config import Config

class TestSupportAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = SupportAssistant()

    def test_retrieve_contexts(self):
        query = "环境增量包有什么用"
        contexts = self.assistant.retrieve_contexts(query)
        self.assertIsNotNone(contexts)
        self.assertGreater(len(contexts), 0)

    def test_query(self):
        query = "Jelina是什么，给我讲解他能干什么"
        response = self.assistant.query(query)
        self.assertIsNotNone(response)
        self.assertIn("Jelina", response)

if __name__ == '__main__':
    unittest.main()