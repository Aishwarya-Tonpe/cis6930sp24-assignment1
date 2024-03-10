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
    # Create a temporary file with phone numbers
    input_text = "John's birthday is on 15th August. Jane's birthday is on 25th July."
    input_file = os.path.join(input_dir, "test_dates.txt")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(input_text)

    # Process the file
    process_file(input_file, output_dir, stats)

    # Verify that the phone numbers are censored
    with open(os.path.join(output_dir, "test_dates.censored"), 'r', encoding='utf-8') as f:
        redacted_text = f.read()
        assert "15th August" not in str(redacted_text)
        print("redacted text", redacted_text)
        assert "25th July" not in str(redacted_text)