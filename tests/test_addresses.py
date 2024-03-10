import os

import pytest
import spacy

import sys

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


    print("Python Version:", sys.version)
    print("SpaCy Version:", spacy.__version__)
    print("SpaCy Models:", spacy.info())
    # Create a temporary file with phone numbers
    input_text = "This is the official address of Universty of Florida Reitz Union - 655 Reitz Union Dr, Gainesville, Florida 32611"
    input_file = os.path.join(input_dir, "test_addresses.txt")
    # input_file = "/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/test_addresses.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(input_text)

    # Process the file
    # output_dir = "/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/output/"
    process_file(input_file, output_dir, stats)

    # Verify that the phone numbers are censored
    # input_file = "/Users/aishwaryatonpe/IdeaProjects/cis6930sp24-assignment1/temp/test_addresses.txt"
    with open(os.path.join(output_dir, "test_addresses.censored"), 'r', encoding='utf-8') as f:
        redacted_text = f.read()
        assert "655 Reitz Union Dr, Gainesville, Florida 32611" not in str(redacted_text)
