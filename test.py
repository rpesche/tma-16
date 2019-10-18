import pytest
import re
import subprocess
import tempfile

from tma_16_assembler import assemble


@pytest.mark.parametrize("source_file,result,report", [
    ('programs/helloworld.asm', 'Hello, world!', {
        'RA': 'A',
        'RB': 0,
        'RC': 0,
        'RD': 0,
        'Stack': "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
        'end_address': 54
    }),
    ])
def test_program_execution(source_file, result, report):
    output_file = tempfile.NamedTemporaryFile(suffix=".tmx")

    assemble(source_file, output_file.name)


    res = subprocess.run([
        'tma-16-rs/target/debug/tma-16-rs',
        output_file.name,
        '--no-display',
        '--report'], capture_output=True)
    assert res

    report_string = res.stdout.decode('utf-8')
    assert report_string

    regex = r"^(.*)$Program terminated at address (\d+) with no error"

    match = re.match(regex, report_string, re.MULTILINE)

    assert match.group(1) == "Hello, world!"
    assert int(match.group(2)) == 54
