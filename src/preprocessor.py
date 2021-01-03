import re

from src.line import Line


class Preprocessor:
    pattern_label_targets = re.compile(r'([\w\d]+):')
    pattern_label_references = re.compile(r'\s:([\w\d]+)\s')

    def __init__(self, input: str):
        self._input = input
        self._processed = ''
        #self._elisions = []

    def get_result(self):
        return self._processed

    def process_labels(self):
        targets = {}
        processed = []
        input = self._input.split('\n')
        line_offset = 0

        # Find all target labels
        for i, line in enumerate(input):
            match_target = self.pattern_label_targets.fullmatch(line)

            if match_target:
                target = match_target.group(1)
                targets[target] = i + 1 - line_offset
                line_offset += 1
            else:
                processed.append((line, i + 1))

        # Find and replace all references to targets
        for i, pair in enumerate(processed):
            line = pair[0]
            line_number = pair[1]
            match_reference = self.pattern_label_references.search(line)

            if match_reference:
                x1 = match_reference.start() + 1  # + 1 to skip the leading whitespace
                x2 = match_reference.end() - 1  # - 1 to skip the trailing whitespace
                ref = match_reference.group(1)

                try:
                    target_line = str(targets[ref])
                except KeyError:
                    # Reference to unknown target
                    error_string = f'Target label "{ref}" does not exist!\n'
                    error_string += f'{line}\n'
                    error_string += f'{x1 * " "}{(x2 - x1) * "^"}\n'
                    error_string += f'(Line {line_number})'
                    raise ValueError(error_string)

                processed[i] = line[:x1] + target_line + line[x2:]

            else:
                processed[i] = line

        self._processed = '\n'.join(processed)
