import io
import typing

def get_file(path: str) -> io.BytesIO:
    with open(path, "rb") as f:
        file = io.BytesIO(f.read())
    return file


def write_file(str_list: typing.List[str], output_path: str) -> None:
    with open(output_path, "a") as f:
        f.writelines(str_list)
