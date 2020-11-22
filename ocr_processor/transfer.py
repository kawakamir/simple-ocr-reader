import io
import typing

from pdf2image import convert_from_bytes


class PDFToJPEG:

    @staticmethod
    def iterate_transform(file: io.BytesIO) -> typing.Iterator[io.BytesIO]:
        pages = convert_from_bytes(file.getvalue())
        for page in pages:
            new_file = io.BytesIO()
            page.save(new_file, "JPEG")
            yield new_file
