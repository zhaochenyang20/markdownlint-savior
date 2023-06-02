import re


input_text = """
# DatasetProcessor Usage

## BaseProcessor

The `BaseProcessor` is a base class for dataset processors. It provides a common interface and defines the necessary methods for post-processing datasets.

To create a dataset processor using the `BaseProcessor`, you need to implement the following method:

- `post_process_example()`: Modifies the input column of a given example dictionary based on the task-specific requirements.

The `BaseProcessor` class can be subclassed to implement custom dataset processing logic based on different task requirements or data formats.

To see an example of how to use `BaseProcessor` and its subclasses, you can refer to the unit tests in the [dataset_processor_test.py](../../tests/dataset_processor_test.py) file.

## TextualizeProcessor

The `TextualizeProcessor` is a dataset processor that converts datasets into a Text2Text fashion. It modifies the input column of each example in the dataset to include task-specific instructions and prefixes.

## Usage

1. Import the necessary modules:

```python
from prompt2model.dataset_processor.textualize import TextualizeProcessor
```

2. Initialize an instance of the `TextualizeProcessor`:

```python
processor = TextualizeProcessor(has_encoder=<True / False>)
```

The `has_encoder` parameter indicates whether the retrieved model has an encoder. For encoder-decoder models like T5, set `has_encoder=True`. For decoder-only models like GPT, set `has_encoder=False`.

"""

def split_into_lines(text):
    lines = []
    current_line = ''
    paragraphs = text.strip().split('\n\n')

    for paragraph in paragraphs:
        if paragraph.startswith("```") and paragraph.endswith("```"):
            lines.append(paragraph)  # Preserve lines between ``` and ```
            lines.append('')  # Add a blank line after preserved lines
        else:
            # Replace ordered list numbers with dashes
            paragraph = re.sub(r'^\d+\.', '-', paragraph, flags=re.MULTILINE)

            words = paragraph.split()
            for word in words:
                if len(current_line) + len(word) <= 80:
                    current_line += word + ' '
                else:
                    lines.append(current_line.strip())
                    current_line = word + ' '

            if current_line:
                lines.append(current_line.strip())
                current_line = ''

            lines.append('')  # Add a blank line between paragraphs

    return lines


def main():
    # User input
    result = split_into_lines(input_text)

    print("Result:")
    for line in result:
        print(line)


if __name__ == "__main__":
    main()
