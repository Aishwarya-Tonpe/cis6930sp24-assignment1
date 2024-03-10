import os

import pytest

from censoror import process_file

@pytest.fixture
def input_dir(tmpdir):
    return str(tmpdir)

@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir)

@pytest.fixture
def stats(tmpdir):
    return str(tmpdir)


def test_phone_numbers_censored(input_dir, output_dir, stats):
    input_text = "John's birthday is on 15th August. Jane's birthday is on 25th July."

    if not os.path.exists("/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/"):
        os.makedirs("/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/")
    input_file = "/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/test_phones.txt"

    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("")

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(input_text)

    # Process the file
    output_dir = "/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/"
    process_file(input_file, output_dir, stats)

    output_file_path = os.path.join(output_dir, "test_phones.censored")

    if not os.path.exists(output_file_path):
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("")

    with open(output_file_path, 'r', encoding='utf-8') as f:
        redacted_text = f.read()
        assert "15th August" not in str(redacted_text)
        print("redacted text", redacted_text)
        assert "25th July" not in str(redacted_text)