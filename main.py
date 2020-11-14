import io
import os

import pyocr
import typing
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

from exceptions import NotSupportExtension, OutputFileAlreadyExist, InputFileDoesNotExist

SUPPORT_EXTENSION = ["png", "jpg", "jepg", "png"]


class PDFToJPEG:

    @staticmethod
    def iterate_transform(file: io.BytesIO) -> typing.Iterator[io.BytesIO]:
        pages = convert_from_bytes(file.getvalue())
        for page in pages:
            new_file = io.BytesIO()
            page.save(new_file, "JPEG")
            yield new_file


class PreProcessor:

    @staticmethod
    def transform(file: io.BytesIO) -> io.BytesIO:
        img = Image.open(file)
        img = img.convert("RGB")
        size = img.size
        img2 = Image.new("RGB", size)
        border = 120
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
    with (output_path, "a") as f:
        f.writelines(str_list)


def main(input_path: str, output_path: str) -> None:
    input_extension = input_path.split(".")[-1]
    output_path_extension = output_path.split(".")[-1]
    if not os.path.exists(input_path):
        raise InputFileDoesNotExist(f"input: {input_path} does not exit")
    if input_extension not in SUPPORT_EXTENSION:
        raise NotSupportExtension(f"input file extension: {input_extension} isn't supported. We support only {SUPPORT_EXTENSION}")
    if output_path_extension == "txt":
        raise NotSupportExtension(f"output file extension: {input_extension} isn't supported. This have to be txt")
    if os.path.exists(output_path):
        raise OutputFileAlreadyExist(f"output: {output_path} is already exist")

    file = get_file(input_path)


    # get_file("./samples/82251504.png")
    PreProcessor().transform()


if __name__ == '__main__':
    main()
    # pages = convert_from_bytes(get_file("./samples/2003.00744v1_image_pdf.pdf").getvalue())
    # for page in pages:
    #     page.save("out.jpg", "JPEG")
