# tests/test_censor_module.py

from censoror import redact_text, process_file
from pydantic import BaseModel
#
# class RedactParams(BaseModel):
#     replacement_char: str = '█'
#
# def redact_text(text, entities, params: RedactParams):
#     for entity in entities:
#         if isinstance(entity, str):
#             text = text.replace(entity, params.replacement_char * len(entity))
#         else:
#             text = text.replace(entity.text, params.replacement_char * len(entity.text))
#     return text

def test_redact_text():
    text = "This is some sensitive information."
    entities = ["sensitive"]
    result = redact_text(text, entities)
    assert "sensitive" not in "This is some ██████████ information."

def test_process_file(tmp_path):
    input_text = "This is some sensitive information."
    input_file = tmp_path / "test_input.txt"
    input_file.write_text(input_text, encoding='utf-8')

    output_directory = tmp_path / "output"
    output_directory.mkdir()

    stats = {'total_files': 0, 'censored_files': [], 'censored_terms': {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0}}

    process_file(input_file, output_directory, stats)

    # Check if the output file is created
    output_file = output_directory / "test_input.censored"
    assert output_file.is_file()

    # Check if statistics are updated
    assert stats['total_files'] == 1
    assert len(stats['censored_files']) == 1
    assert stats['censored_terms']['names'] == 0
    assert stats['censored_terms']['dates'] == 0
    assert stats['censored_terms']['phones'] == 0
    assert stats['censored_terms']['addresses'] == 0
