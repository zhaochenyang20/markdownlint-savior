import re


input_text = """
# DatasetRetriever

## Overview

- `DatasetRetriever`: Interface for retrieving datasets based on a prompt.
- `DescriptionDatasetRetriever`: Retrieves HuggingFace datasets using similarity to a given prompt.

## Getting Started

- Import Modules

```python
from prompt2model.dataset_retriever import DescriptionDatasetRetriever
from prompt2model.prompt_parser import MockPromptSpec, TaskType
```

- Initialize Retriever

```python
retriever = DescriptionDatasetRetriever()
```

Various parameters like search index path, model name, and search depth can be customized during initialization.

- Prepare the Prompt

```python
task_type = TaskType.TEXT_GENERATION
prompt_text = "..."
prompt_spec = MockPromptSpec(task_type)
prompt_spec._instruction = prompt_text
```

- Retrieve Dataset

```python
dataset_dict = retriever.retrieve_dataset_dict(
    prompt_spec, blocklist=[]
)
```

`dataset_dict` will contain the dataset splits (train/val/test) most relevant to the given prompt.

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

            # Handle lines starting with '-'
            if paragraph.startswith('-'):
                sublines = paragraph.split('\n')
                for subline in sublines:
                    words = subline.split()
                    for word in words:
                        # Check if line length exceeds the limit
                        if len(current_line) + len(word) <= 70:
                            current_line += word + ' '
                        else:
                            lines.append(current_line.strip())
                            current_line = word + ' '

                    if current_line:
                        lines.append(current_line.strip())
                        current_line = ''

                lines.append('')  # Add a blank line after preserved lines
                continue

            words = paragraph.split()
            for word in words:
                if len(current_line) + len(word) <= 70:
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
    for line in result:
        print(line)


if __name__ == "__main__":
    main()
