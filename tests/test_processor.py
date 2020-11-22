import io

import pytest

from file_operators import get_file
from processor import ocr_precess, PreProcessor, OCRTesseractProcessor, PostProcessor


def test_pre_processor():
    file = get_file("tests/test_sample/82251504.png")
    new_file = PreProcessor(100).transform(file)
    assert type(new_file) == io.BytesIO


def test_ocr_tesseract_processor():
    file = get_file("tests/test_sample/82251504.png")
    text = OCRTesseractProcessor().transform(file)
    assert type(text) == str


def test_post_processor():
    text1 = "asb√sss"
    text2 = "asb-sss"
    new_text1 = PostProcessor().transform(text1)
    new_text2 = PostProcessor().transform(text2)
    assert new_text1 == "asbsss"
    assert new_text2 == "asb-sss"


def test_ocr_processor():
    file = get_file("tests/test_sample/82251504.png")
    fixed_text = ocr_precess(file, PreProcessor(100), OCRTesseractProcessor(), PostProcessor())
    assert type(fixed_text) == str
