from PyPDF2.utils import PdfReadWarning

import warnings
warnings.filterwarnings("ignore", category=PdfReadWarning)

import os
import csv
import sys
import PyPDF2

def main(args):
    input_file, output_dir, password_file = get_args(args)
    split_pdf_with_passwords(input_file, output_dir, password_file)

def get_args(args):
    if len(args) != 4:
        print(f"Usage: {args[0]} <input_file> <output_dir> <password_csv>")
        sys.exit(1)

    input_file = args[1]
    output_dir = args[2]
    password_file = args[3]

    if not os.path.isfile(input_file):
        print(f"{input_file} does not exist or is not a file")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"{output_dir} does not exist or is not a directory")
        sys.exit(1)

    if not os.path.isfile(password_file):
        print(f"{password_file} does not exist or is not a file")
        sys.exit(1)

    return input_file, output_dir, password_file

def split_pdf_with_passwords(input_file, output_dir, password_file):
    with open(password_file) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for page_num, row in enumerate(csvreader, start=1):
            password = row[0]
            output_file = os.path.join(output_dir, f"page-{page_num}.pdf")
            with open(input_file, "rb") as pdf_file, open(output_file, "wb") as output:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                pdf_writer = PyPDF2.PdfFileWriter()
                pdf_writer.addPage(pdf_reader.getPage(page_num-1))
                pdf_writer.encrypt(password, use_128bit=True)
                pdf_writer.write(output)

def print_usage():
    print(f"Usage: {sys.argv[0]} <input_file> <output_dir> <password_csv>")

if __name__ == "__main__":
    main(sys.argv)
