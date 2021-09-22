import pathlib
import random
import string
import tempfile

from PyPDF2 import PdfFileReader
from word_search_generator import config
from word_search_generator import utils
from word_search_generator.export import write_pdf_file


TEMP_DIR = tempfile.TemporaryDirectory()


def generate_test_key(length: int):
    """Generate a test answer key of size `length`."""
    key = {}
    for i in range(length):
        word = utils.get_random_words(1)
        start = (random.randint(0, 9), random.randint(0, 9))
        direction = random.choice(list(config.dir_moves))
        key[word] = {"start": start, "direction": direction}
    return key


def test_export_pdf_puzzles():
    """Export a bunch of puzzles as PDF and make sure they are all 1-page."""
    sizes = [s for s in range(config.min_puzzle_size, config.max_puzzle_size)]
    keys = [k for k in range(3, config.max_puzzle_words, 9)]
    for s in sizes:
        for k in keys:
            puzzle = [["X"] * s for _ in range(s)]
            key = generate_test_key(k)
            level = random.randint(1, 3)
            path = pathlib.Path(f"{TEMP_DIR.name}/test_s{s}_l{level}_k{len(key)}.pdf")
            write_pdf_file(path, puzzle, key, level)
            pdf = PdfFileReader(open(path, "rb"))
            assert pathlib.Path(path).exists() and pdf.getNumPages() == 1