from unittest import TestCase

from src.preprocessor import Preprocessor


class TestPreProcessor(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_instance(self):
        input = ""

        _uut = Preprocessor(input)

    def test_process_labels(self):
        input = ('jump :label1 notEqual @unit null\n'
                 'ubind @mono\n'
                 'label1:\n'
                 'end')
        expected = ('jump 3 notEqual @unit null\n'
                    'ubind @mono\n'
                    'end')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_unreferenced_target(self):
        input = ('jump 5 notEqual @unit null\n'
                 'ubind @mono\n'
                 'label1:\n'
                 'end')
        expected = ('jump 5 notEqual @unit null\n'
                    'ubind @mono\n'
                    'end')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_target_does_not_exist(self):
        input = ('jump :label1 notEqual @unit null\n'
                 'ubind @mono\n'
                 'end')

        uut = Preprocessor(input)
        with self.assertRaises(ValueError):
            uut.process_labels()

    def test_process_labels_target_two_labels(self):
        input = ('label1:\n'
                 'jump :label2 notEqual @unit null\n'
                 'ubind @mono\n'
                 'label2:\n'
                 'jump :label1 notEqual @unit null\n'
                 'end')
        expected = ('jump 3 notEqual @unit null\n'
                    'ubind @mono\n'
                    'jump 1 notEqual @unit null\n'
                    'end')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_target_five_labels(self):
        input = ('jump :label1 notEqual @unit null\n'
                 'label1:\n'
                 'label2:\n'
                 'jump :label2 notEqual @unit null\n'
                 'ubind @mono\n'
                 'label3:\n'
                 'jump :label5 notEqual @unit null\n'
                 'label4:\n'
                 'end\n'
                 'jump :label4 notEqual @unit null\n'
                 'label5:\n'
                 'jump :label3 notEqual @unit null\n')

        expected = ('jump 2 notEqual @unit null\n'
                    'jump 2 notEqual @unit null\n'
                    'ubind @mono\n'
                    'jump 7 notEqual @unit null\n'
                    'end\n'
                    'jump 5 notEqual @unit null\n'
                    'jump 4 notEqual @unit null\n')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_consecutive_targets(self):
        input = ('jump :label2 notEqual @unit null\n'
                 'ubind @mono\n'
                 'label1:\n'
                 'label2:\n'
                 'label3:\n'
                 'end')
        expected = ('jump 3 notEqual @unit null\n'
                    'ubind @mono\n'
                    'end')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

# TODO: Regex-test error message for references to unknown targets (line number, chevrons, etc.)
