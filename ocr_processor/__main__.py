import io
import os
import typing
from logging import DEBUG, WARNING, Logger, basicConfig, getLogger

import click
from pdf2image import convert_from_bytes

from file_operators import get_file, write_file
from processors import (PostProcessor, PreProcessor, OCRTesseractProcessor, ocr_precess)

SUPPORT_INPUT_EXTENSIONS = ["pdf", "jpg", "jepg", "png"]
SUPPORT_OUTPUT_EXTENSIONS = ["txt", "text"]
RGB_BORDER = 120




def setup_logger(verbose: bool) -> Logger:
    if verbose:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=WARNING)
    logger = getLogger(__name__)
    return logger

def validation_input_path(input_path: str, input_extension, support_input_extensions: typing.List[str]) -> None:
    if not os.path.exists(input_path):
        raise click.BadParameter(f"input: {input_path} does not exit")
    if input_extension not in support_input_extensions:
        raise click.BadParameter(
            f"input file extension: {input_extension} isn't supported. We support only {support_input_extensions}")

def validation_output_path(output_path: str, output_extension: str, support_output_extensions: typing.List[str]) -> None:
    if output_extension not in support_output_extensions:
        raise click.BadParameter(f"output file extension: {output_extension} isn't supported. This have to be txt")
    if os.path.exists(output_path):
        raise click.BadParameter(f"output: {output_path} is already exist")


@click.command()
@click.option("--input", "input_path", type=str, help="path of input file")
@click.option("--output", "output_path", type=str, help="path of output file")
@click.option("--verbose", is_flag=True, help="output detailed logs")
def main(input_path: str, output_path: str, verbose: bool) -> None:
    logger = setup_logger(verbose)
    logger.info("start ocr process")

    input_extension = input_path.split(".")[-1]
    output_extension = output_path.split(".")[-1]
    validation_input_path(input_path, input_extension, SUPPORT_INPUT_EXTENSIONS)
    validation_output_path(output_path, output_extension, SUPPORT_OUTPUT_EXTENSIONS)

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
