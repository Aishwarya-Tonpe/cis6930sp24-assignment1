import os

import pytest

from censoror import process_file

@pytest.fixture
def input_dir(tmpdir):
    print("TEMP DIR", tmpdir)
    return str(tmpdir)

@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir)

@pytest.fixture
def stats(tmpdir):
    return str(tmpdir)


def test_phone_numbers_censored(input_dir, output_dir, stats):
    # Create a temporary file with phone numbers
    input_text = "John's phone number is 555-222-1234. Jane's phone number is 555-665-5678. Please contact them."
    input_file = os.path.join(input_dir, "test_phone_numbers.txt")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(input_text)

    print("&&&&&&&&&", output_dir, "nnn", input_dir)
    # Process the file
    process_file(input_file, output_dir, stats)

    # Verify that the phone numbers are censored
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, "test_phone_numbers.censored"), 'r', encoding='utf-8') as f:
        redacted_text = f.read()
        assert "555-222-1234" not in str(redacted_text)
        print("redacted text", redacted_text)
        assert "555-665-5678" not in str(redacted_text)