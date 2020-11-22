import io
import re
from logging import DEBUG, WARNING, Logger, basicConfig, getLogger

import click
import pyocr
from file_operators import get_file, write_file
from PIL import Image
from transfer import PDFToJPEG
from validations import validation_input_path, validation_output_path

SUPPORT_INPUT_EXTENSIONS = ["pdf", "jpg", "jepg", "png"]
SUPPORT_OUTPUT_EXTENSIONS = ["txt", "text"]
RGB_BORDER = 120


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


def setup_logger(verbose: bool) -> Logger:
    if verbose:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=WARNING)
    logger = getLogger(__name__)
    return logger


@click.command()
@click.option("--input", "input_path", type=str, help="path of input file", required=True)
@click.option("--output", "output_path", type=str, help="path of output file", required=True)
@click.option("--verbose", is_flag=True, help="output detailed logs")
def main(input_path: str, output_path: str, verbose: bool) -> None:
    logger = setup_logger(verbose)
    logger.info("start ocr process")

    input_extension = input_path.split(".")[-1]
    validation_input_path(input_path, SUPPORT_INPUT_EXTENSIONS)
    validation_output_path(output_path, SUPPORT_OUTPUT_EXTENSIONS)

    lines = []
    input_file = get_file(input_path)
    if input_extension == "pdf":
        logger.info("start converting pdf to string")
        for i, file in enumerate(PDFToJPEG().iterate_transform(input_file), 1):
            lines.append(ocr_precess(file, PreProcessor(RGB_BORDER), OCRTesseractProcessor(), PostProcessor()))
            file.close()
            logger.info(f"finish converting pdf to string, at {i} page")
    else:
        logger.info(f"start converting {input_extension} to string")
        lines.append(ocr_precess(input_file, PreProcessor(RGB_BORDER), OCRTesseractProcessor(), PostProcessor()))
        logger.info(f"finish converting {input_extension} to string")
    input_file.close()

    logger.info(f"start converting string to text file")
    write_file(lines, output_path)
    logger.info(f"start converting string to text file")
    logger.info(f"finish ocr processing")


if __name__ == '__main__':
    main()
