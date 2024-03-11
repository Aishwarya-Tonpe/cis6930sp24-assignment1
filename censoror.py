import re
import spacy
import argparse
import os
import glob
import sys
from collections import defaultdict
import pyap
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def censor_text(text, entities, replacement_char='█'):
    for entity in entities:
        if isinstance(entity, str):
            text = text.replace(entity, replacement_char * len(entity))

        else:
            text = text.replace(entity.text, replacement_char * len(entity.text))
    return text

def process_file(file_path, output_directory, stats):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        try:
            nlp = spacy.load("en_core_web_sm")
        except IOError:
            print("SpaCy model not found. Downloading...")
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

        doc = nlp(text)

        phone_number_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
        address_pattern = re.compile(r'\b\d{1,5}\s\w+\s\w+(\s\w+)?,\s\w+,\s\w+,\s\d{5}\b')
        date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        name_pattern = re.compile(r'\b[A-Z][a-z]*\b')

        # Extract entities based on flags
        names = [ent for ent in doc.ents if ent.label_ == 'PERSON']
        dates = [ent for ent in doc.ents if ent.label_ == 'DATE']
        # phones = [ent for ent in doc.ents if ent.label_ == 'PHONE']
        phones = re.findall(phone_number_pattern, text)
        # addresses = [ent for ent in doc.ents if ent.label_ == 'ADDRESS']
        extract_addresses = pyap.parse(text, country='US')
        addresses = [str(address) for address in extract_addresses]

        date_matches = re.findall(date_pattern, text)
        phone_numbers = re.findall(phone_number_pattern, text)

        tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
        model = AutoModelForTokenClassification.from_pretrained("ctrlbuzz/bert-addresses")
        nlp2 = pipeline("ner", model=model, tokenizer=tokenizer)
        addresses_hf = [entity['word'] for entity in nlp2(text) if entity['entity'] == 'ADDRESS']

        # Censor sensitive information
        censored_text = censor_text(text, addresses + addresses_hf + names + dates + date_matches + phones + phone_numbers)

        # Save redacted file
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_directory, f"{file_name}.censored")
        with open(output_path, 'w', encoding='utf-8') as redacted_file:
            redacted_file.write(censored_text)

# Update statistics
        stats['total_files'] += 1
        stats['censored_files'].append(output_path)
        stats['censored_terms']['names'] += len(names)
        stats['censored_terms']['dates'] += len(dates)
        stats['censored_terms']['phones'] += len(phones)
        stats['censored_terms']['addresses'] += len(addresses)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}", file=sys.stderr)

def generate_stats(stats, redacted_texts, stats_output):
    with open(stats_output, 'w', encoding='utf-8') as stats_file:
        stats_file.write(f"Total processed files: {stats['total_files']}\n\n")
        stats_file.write("Censored Terms:\n")
        for term, count in stats['censored_terms'].items():
            stats_file.write(f"{term.capitalize()}: {count}\n")

        stats_file.write("\nCensored Files:\n")
        for censored_file in stats['censored_files']:
            if isinstance(censored_file, str):  # Check if it's a string
                stats_file.write(f"File: {censored_file}\n")
            else:
                stats_file.write(f"File: {censored_file['file_path']}\n")

def main():
    parser = argparse.ArgumentParser(description="Censor sensitive information in plain text documents.")
    parser.add_argument('--input', nargs='+', help="Input files using glob patterns.")
    parser.add_argument('--output', help="Output directory for censored files.")
    parser.add_argument('--names', action='store_true', help="Censor names.")
    parser.add_argument('--dates', action='store_true', help="Censor dates.")
    parser.add_argument('--phones', action='store_true', help="Censor phone numbers.")
    parser.add_argument('--address', action='store_true', help="Censor addresses.")
    parser.add_argument('--stats', type=str, default='stderr', help="Statistics output destination.")

    args = parser.parse_args()

    if not args.input:
        print("Please provide input files using --input flag.")
        sys.exit(1)

    output_directory = args.output
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    entities_to_censor = []
    if args.names:
        entities_to_censor.append('PERSON')
    if args.dates:
        entities_to_censor.append('DATE')
    if args.phones:
        entities_to_censor.append('PHONE')
    if args.address:
        entities_to_censor.append('ADDRESS')

    stats = {'total_files': 0, 'censored_files': [], 'censored_terms': defaultdict(int)}

    redacted_texts = []
    for pattern in args.input:
        files = glob.glob(pattern)
        print("FILE", files)
        for file_path in files:
            redacted_text = process_file(file_path, args.output, stats)
            redacted_texts.append(f"File: {file_path}\n{redacted_text}")

    if args.stats == 'stderr':
        print("Statistics:\n", stats, file=sys.stderr)
    elif args.stats == 'stdout':
        print("Statistics:\n", stats)
    else:
        generate_stats(stats, redacted_texts, args.stats)

if __name__ == "__main__":
    main()
