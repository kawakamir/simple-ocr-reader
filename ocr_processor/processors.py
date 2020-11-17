import io
import re
import typing

import pyocr
from pdf2image import convert_from_bytes
from PIL import Image


class PDFToJPEG:

    @staticmethod
    def iterate_transform(file: io.BytesIO) -> typing.Iterator[io.BytesIO]:
        pages = convert_from_bytes(file.getvalue())
        for page in pages:
            new_file = io.BytesIO()
            page.save(new_file, "JPEG")
            yield new_file


class PreProcessor:

    def __init__(self, rgb_border: int) -> None:
        self.rgb_border = rgb_border

    def transform(self, file: io.BytesIO) -> io.BytesIO:
        img = Image.open(file)
        img = img.convert("RGB")
        size = img.size
        img2 = Image.new("RGB", size)
        border = self.rgb_border
        for x in range(size[0]):
            for y in range(size[1]):
                r, g, b = img.getpixel((x, y))
                if r > border or g > border or b > border:
                    r = 255
                    g = 255
                    b = 255
                img2.putpixel((x, y), (r, g, b))
        return file


class OCRTesseractProcessor:

    @staticmethod
    def transform(file: io.BytesIO) -> str:
        tools = pyocr.get_available_tools()
        tool = tools[0]
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        text = tool.image_to_string(Image.open(file), builder=builder)
        return text


class PostProcessor:

    @classmethod
    def transform(cls, text: str) -> str:
        m = re.findall("[a-zA-Z_0-9\-\]\[{}():~,/; \n\.]", text)
        new_text = ""
        if m:
            new_text = "".join(m)
        return new_text


def ocr_precess(file: io.BytesIO, pre_processor: PreProcessor, oct_tesseract_processor: OCRTesseractProcessor,
                post_processor: PostProcessor) -> str:
    fixed_file = pre_processor.transform(file)
    text = oct_tesseract_processor.transform(fixed_file)
    fixed_file.close()
    fixed_text = post_processor.transform(text)
    return fixed_text
