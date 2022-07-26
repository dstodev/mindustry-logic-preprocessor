
from inspect import cleandoc
from test.samples import *
from unittest import TestCase

from src.preprocessor import Preprocessor


class TestPreProcessor(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_instance(self):
        input = ''

        _uut = Preprocessor(input)

    def test_process_labels(self):
        input = CUSTOM_SIMPLE
        expected = STANDARD_SIMPLE

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_unreferenced_target(self):
        input = cleandoc('''
            jump 2 notEqual @unit null
            ubind @mono
            label1:
            end
        ''')
        expected = STANDARD_SIMPLE

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_target_does_not_exist(self):
        input = cleandoc('''
            jump :label1 notEqual @unit null
            ubind @mono
            end
        ''')

        uut = Preprocessor(input)

        with self.assertRaises(ValueError):
            uut.process_labels()

    def test_process_labels_target_two_labels(self):
        input = cleandoc('''
            label1:
            jump :label2 notEqual @unit null
            ubind @mono
            label2:
            jump :label1 notEqual @unit null
            end
        ''')
        expected = cleandoc('''
            jump 2 notEqual @unit null
            ubind @mono
            jump 0 notEqual @unit null
            end
        ''')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_target_five_labels(self):
        input = cleandoc('''
            jump :label1 notEqual @unit null
            label1:
            label2:
            jump :label2 notEqual @unit null
            ubind @mono
            label3:
            jump :label5 notEqual @unit null
            label4:
            end
            jump :label4 notEqual @unit null
            label5:
            jump :label3 notEqual @unit null
        ''')
        expected = cleandoc('''
            jump 1 notEqual @unit null
            jump 1 notEqual @unit null
            ubind @mono
            jump 6 notEqual @unit null
            end
            jump 4 notEqual @unit null
            jump 3 notEqual @unit null
        ''')

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_consecutive_targets(self):
        input = cleandoc('''
            jump :label2 notEqual @unit null
            ubind @mono
            label1:
            label2:
            label3:
            end
        ''')
        expected = STANDARD_SIMPLE

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_empty_lines(self):
        input = cleandoc('''
            jump :label1 notEqual @unit null
            ubind @mono

            label1:

            end
        ''')
        expected = STANDARD_SIMPLE

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)

    def test_process_labels_bad_target_error_line_number_simple_program(self):
        input = cleandoc('''
            jump :label1 notEqual @unit null
            ubind @mono
            end
        ''')

        uut = Preprocessor(input)

        with self.assertRaisesRegex(ValueError, r'Line 1'):
            uut.process_labels()

    def test_process_labels_bad_target_error_line_number_between_other_targets(self):
        input = cleandoc('''
            jump :label1 notEqual @unit null
            label1:
            label2:
            jump :label2 notEqual @unit null
            ubind @mono
            label3:
            jump :label5 notEqual @unit null
            end
            jump :label4 notEqual @unit null
            label5:
            jump :label3 notEqual @unit null
        ''')

        uut = Preprocessor(input)

        with self.assertRaisesRegex(ValueError, r'Line 9'):
            uut.process_labels()

    def test_parse_lines(self):
        pass

    def test_complex(self):
        input = CUSTOM_COMPLEX
        expected = STANDARD_COMPLEX

        uut = Preprocessor(input)
        uut.process_labels()

        actual = uut.get_result()

        self.assertEqual(expected, actual)


# TODO: Regex-test error message for references to unknown targets (line number, chevrons, etc.)
# TODO: Consume empty lines but keep track of removed lines for offsetting purposes
