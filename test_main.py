import pytest
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path


@pytest.mark.parametrize(
    'input_str,country_code,expected_str',
    [
        (
            'TEL;type=CELL;type=VOICE;type=pref:03 000 000',
            961,
            'TEL;type=CELL;type=VOICE;type=pref:+9613000000'
        ),
        (
            'TEL;type=CELL;type=VOICE;type=pref:71 000 000',
            961,
            'TEL;type=CELL;type=VOICE;type=pref:+96171000000'
        ),
        (
            'TEL;type=pref:+9631000000',
            961,
            'TEL;type=pref:+9631000000'
        ),
        (
            'TEL;type=pref:009631000000',
            961,
            'TEL;type=pref:009631000000'
        ),
        (
            'END:VCARD',
            961,
            'END:VCARD'
        ),
        (
            'TEL;type=CELL;type=VOICE;type=pref:03 000 000\nEND:VCARD\nTEL;type=CELL;type=VOICE;type=pref:71 000 000',
            961,
            'TEL;type=CELL;type=VOICE;type=pref:+9613000000\nEND:VCARD\nTEL;type=CELL;type=VOICE;type=pref:+96171000000'
        )
    ]
)
def test_main(input_str: str, country_code: int, expected_str: str) -> None:

    with patch.multiple('click', command=MagicMock(return_value=lambda func: func)):
        with patch.multiple(
            'main',
            open=mock_open(read_data=input_str),
        ):
            from main import main
            returned_str = main(input_file='some_path', output_file='some_path', country_code=country_code)
            assert expected_str == returned_str


@pytest.mark.parametrize(
    'input_file,output_file,country_code,error_key',
    [
        (
            'some/file/path/that/doesnt/exist.vcf',
            'some/file/path/that/doesnt/exist_updated.vcf',
            961,
            'ifile_file'
        ),
        (
            'some/file/path/that/doesnt/exist.py',
            'some/file/path/that/doesnt/exist_updated.py',
            961,
            'ifile_extension'
        ),
        (
            'some/file/path/that/doesnt/exist.py',
            str(Path(__file__).resolve().parent),
            961,
            'ofile_dir'
        ),
        (
            'some/file/path/that/doesnt/exist.vcf',
            'some/file/path/that/doesnt/exist.vcf',
            961,
            'iofile_equal'
        ),
        (
            'some/file/path/that/doesnt/exist.vcf',
            'some/file/path/that/doesnt/exist_updated.vcf',
            -961,
            'cc_negative'
        ),
    ]
)
def test_validator_fail(input_file: str, output_file: str, country_code: int, error_key: str) -> None:
    with patch('click.echo') as mock_echo:
        from main import ValidatorCommand, error_messages
        ctx = MagicMock()
        ctx.params = dict(input_file=input_file, output_file=output_file, country_code=country_code)

        with pytest.raises(SystemExit) as e:
            ValidatorCommand(name='test')._validate(ctx=ctx)

        mock_echo.assert_any_call(error_messages[error_key])


@pytest.mark.parametrize(
    'input_file,output_file,country_code',
    [
        (
            str(__file__).replace('.py', '.vcf'),
            'some/file/path/that/doesnt/exist_updated.vcf',
            961
        )
    ]
)
def test_validator_success(input_file: str, output_file: str, country_code: int) -> None:

    with patch('pathlib.Path.is_file', MagicMock(return_value=True)):
        from main import ValidatorCommand
        ctx = MagicMock()
        ctx.params = dict(input_file=input_file, output_file=output_file, country_code=country_code)
        ValidatorCommand(name='test')._validate(ctx=ctx)