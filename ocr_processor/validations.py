import os
import typing

import click


def validation_input_path(input_path: str, support_input_extensions: typing.List[str]) -> None:
    if len(input_path.split(".")) == 1:
        raise click.BadParameter(f"input_path should be file")
    input_extension = input_path.split(".")[-1]
    if not os.path.exists(input_path):
        raise click.BadParameter(f"input: {input_path} does not exit")
    if input_extension not in support_input_extensions:
        raise click.BadParameter(
            f"input file extension: {input_extension} isn't supported. We support only {support_input_extensions}")


def validation_output_path(output_path: str, support_output_extensions: typing.List[str]) -> None:
    if len(output_path.split(".")) == 1:
        raise click.BadParameter(f"input_path should be file")
    output_extension = output_path.split(".")[-1]
    if output_extension not in support_output_extensions:
        raise click.BadParameter(f"output file extension: {output_extension} isn't supported. This have to be txt")
    if os.path.exists(output_path):
        raise click.BadParameter(f"output: {output_path} is already exist")
