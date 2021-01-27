import sys
import re
import click
from pathlib import Path

options = {
    'input': {
        'short': 'i',
        'long': 'input_file',
        'help': 'absolute .vcf input file path'
    },
    'output': {
        'short': 'o',
        'long': 'output_file',
        'help': 'absolute modified .vcf file path'
    },
    'code': {
        'short': 'c',
        'long': 'country_code',
        'help': 'country code'
    }
}

error_messages = {
    'ifile_file': 'Please provide an input FILE path!',
    'ifile_extension': 'This script only works with .vcf files!',
    'ofile_dir': 'Please provide an output FILE path!',
    'iofile_equal': 'Please choose different file paths for input and output as this will overwrite your input file.',
    'cc_negative': 'There are no negative country codes on earth yet ;)'
}


class ValidatorCommand(click.Command):

    def invoke(self, ctx) -> None:
        self._validate(ctx)
        super().invoke(ctx)

    def _validate(self, ctx) -> None:

        input_file_path = Path(ctx.params[options['input']['long']])
        output_file_path = Path(ctx.params[options['output']['long']])
        country_code: int = ctx.params[options['code']['long']]

        errors = []

        if not input_file_path.is_file():
            errors.append(error_messages['ifile_file'])

        if not input_file_path.suffix == '.vcf':
            errors.append(error_messages['ifile_extension'])

        if output_file_path.is_dir():
            errors.append(error_messages['ofile_dir'])

        if input_file_path == output_file_path:
            errors.append(error_messages['iofile_equal'])

        if country_code < 0:
            errors.append(error_messages['cc_negative'])

        if errors:
            click.echo(click.style('Validation failed!', fg='red', bold=True))
            for error in errors:
                click.echo(error)
            sys.exit(1)


@click.command(
    cls=ValidatorCommand,
    help='Add the provided country code to every contact phone number in a .vcf file if a country code is not found for'
         ' that phone number.',
)
@click.option(
    f'-{options["input"]["short"]}', f'--{options["input"]["long"]}', help=options["input"]["help"],
    required=True, type=str,
)
@click.option(
    f'-{options["output"]["short"]}', f'--{options["output"]["long"]}', help=options["output"]["help"],
    required=True, type=str,
)
@click.option(
    f'-{options["code"]["short"]}', f'--{options["code"]["long"]}', help=options["code"]["help"],
    required=True, type=int,
)
def main(input_file: str, output_file: str, country_code: int) -> str:

    with open(input_file) as file:
        data_str = file.read()

    pattern = re.compile(r'^(?P<info>TEL.*:)(?P<number>(?!00)(?!\+).+)$')

    def repl(match: re.Match):
        number = match.group('number')
        number: str = number[1:] if number[0] == '0' else number
        return f'{match.group("info")}+{country_code}{number.replace(" ", "")}'

    data_str = re.sub(
        pattern=pattern.pattern,
        repl=repl,
        string=data_str,
        flags=re.MULTILINE
    )

    if re.findall(pattern=pattern.pattern, string=data_str, flags=re.MULTILINE):
        click.echo(click.style(text='Something went wrong, better not continue :(', fg='red'))
        sys.exit(2)

    click.echo(f'Writing new data to {output_file} ...')

    with open(output_file, 'w+') as file:
        file.write(data_str)

    return data_str


if __name__ == '__main__':
    main()
