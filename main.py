import io
import os
from logging import getLogger, DEBUG, Logger, basicConfig, WARNING

import click
import pyocr
import typing
from PIL import Image
from pdf2image import convert_from_bytes


SUPPORT_INPUT_EXTENSION = ["pdf", "jpg", "jepg", "png"]
SUPPORT_OUTPUT_EXTENSION = ["txt", "text"]
RGB_BORDER = 120


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
    def transform(file: io.BytesIO) -> typing.List[str]:
        tools = pyocr.get_available_tools()
        tool = tools[0]
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        lines = tool.image_to_string(Image.open(file), builder=builder)
        return lines


class PostProcessor:

    @classmethod
    def transform(cls, lines: typing.List[str]) -> typing.List[str]:
        return lines


def ocr_precess(file: io.BytesIO, pre_processor: PreProcessor, oct_tesseract_processor: OCRTesseractProcessor,
                post_processor: PostProcessor) -> typing.List[str]:
    fixed_file = pre_processor.transform(file)
    lines = oct_tesseract_processor.transform(fixed_file)
    fixed_file.close()
    fixed_lines = post_processor.transform(lines)
    return fixed_lines


def get_file(path: str) -> io.BytesIO:
    with open(path, "rb") as f:
        file = io.BytesIO(f.read())
    return file


def write_file(str_list: typing.List[str], output_path: str) -> None:
    with open(output_path, "a") as f:
        f.writelines(str_list)


def setup_logger(verbose: bool) -> Logger:
    if verbose:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=WARNING)
    logger = getLogger(__name__)
    return logger


@click.command()
@click.option("--input", "input_path", type=str, help="path of input file")
@click.option("--output", "output_path", type=str, help="path of output file")
@click.option("--verbose", is_flag=True, help="output detailed logs")
def main(input_path: str, output_path: str, verbose: bool) -> None:
    input_extension = input_path.split(".")[-1]
    output_path_extension = output_path.split(".")[-1]
    if not os.path.exists(input_path):
        raise click.BadParameter(f"input: {input_path} does not exit")
    if input_extension not in SUPPORT_INPUT_EXTENSION:
        raise click.BadParameter(
            f"input file extension: {input_extension} isn't supported. We support only {SUPPORT_INPUT_EXTENSION}")
    if output_path_extension not in SUPPORT_OUTPUT_EXTENSION:
        raise click.BadParameter(f"output file extension: {input_extension} isn't supported. This have to be txt")
    if os.path.exists(output_path):
        raise click.BadParameter(f"output: {output_path} is already exist")

    logger = setup_logger(verbose)
    logger.info("start ocr process")
    input_extension = input_path.split(".")[-1]

    lines = []
    input_file = get_file(input_path)
    if input_extension == "pdf":
        logger.info("start processing pdf to string")
        for i, file in enumerate(PDFToJPEG().iterate_transform(input_file), 1):
            lines.extend(ocr_precess(file, PreProcessor(RGB_BORDER), OCRTesseractProcessor(), PostProcessor()))
            file.close()
            logger.info(f"finish processing pdf to string, at {i} page")
    else:
        logger.info(f"start processing {input_extension} to string")
        lines.extend(ocr_precess(input_file, PreProcessor(RGB_BORDER), OCRTesseractProcessor(), PostProcessor()))
        logger.info(f"finish processing {input_extension} to string")

    logger.info(f"start processing string to text file")
    write_file(lines, output_path)
    logger.info(f"start processing string to text file")
    input_file.close()
    logger.info(f"finish ocr processing")


if __name__ == '__main__':
    main()
