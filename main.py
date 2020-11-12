import io

import pyocr
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes


def get_file(path: str) -> bin:
    with open(path, "rb") as f:
        file = io.BytesIO(f.read())
    return file

def write_file(path: str, file: str):
    pass

class PreProcessor:
    def transform(self, ):
        tools = pyocr.get_available_tools()
        tool = tools[0]
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        lines = tool.image_to_string(Image.open(get_file("./samples/test_scan.jpg")), builder=builder)
        print(lines)

class OCRTesseract:
    def transform(self, file_data: bin):
        pass

class PostProcessor:
    def transform(self, text_data: bin):
        pass


def main():
    # get_file("./samples/82251504.png")
    PreProcessor().transform()

if __name__ == '__main__':
    main()
    # pages = convert_from_bytes(get_file("./samples/2003.00744v1_image_pdf.pdf").getvalue())
    # for page in pages:
    #     page.save("out.jpg", "JPEG")

