import click

from .converter import MarkdownConverter


@click.argument("savedir", type=click.Path(exists=True))
@click.argument("fn", type=click.STRING)
@click.command("convert", short_help="Convert HTML to Markdown")
def run_convert(fn, savedir):
    """HTML 파일을 마크다운으로 변환합니다.

    이 명령은 지정된 HTML 파일을 읽고, 마크다운 형식으로 변환한 후,
    지정된 디렉토리에 결과 파일을 저장합니다.

    Args:\n
        fn (str): 변환할 HTML 파일의 경로.\n
        savedir (str): 변환된 마크다운 파일을 저장할 디렉토리의 경로.\n
    """
    converter = MarkdownConverter(savedir)
    converter.convert(fn)
