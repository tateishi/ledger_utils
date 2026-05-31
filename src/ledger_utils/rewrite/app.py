from pathlib import Path

import typer

from . import comma_convert, plain_convert
from .common import compute_output_path, convert_one_file, do_rewrite

app = typer.Typer(help="Rewrite related command.")


@app.command("plain")
def rewrite_plain(
    input_dir: Path = typer.Option(None, "-i", "--input_dir", help="入力ディレクトリ"),
    output_dir: Path = typer.Option(
        None,
        "-o",
        "--output_dir",
        help="出力ディレクトリ（未指定なら入力ファイルを上書き）",
    ),
    encoding: str = typer.Option(
        "utf-8", "-e", "--encoding", help="読み書きの文字コード（デフォルト: utf-8）"
    ),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="書き込みせず、変換対象だけ表示"
    ),
) -> int:

    if input_dir is None:
        print(f"ERROR: input_dir is not a directory: {input_dir}", file=sys.stderr)
        return 2

    return do_rewrite(input_dir, output_dir, encoding, dry_run, plain_convert)


@app.command("comma")
def rewrite_comma(
    input_dir: Path = typer.Option(None, "-i", "--input_dir", help="入力ディレクトリ"),
    output_dir: Path = typer.Option(
        None,
        "-o",
        "--output_dir",
        help="出力ディレクトリ（未指定なら入力ファイルを上書き）",
    ),
    encoding: str = typer.Option(
        "utf-8", "-e", "--encoding", help="読み書きの文字コード（デフォルト: utf-8）"
    ),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="書き込みせず、変換対象だけ表示"
    ),
) -> int:

    if input_dir is None:
        print(f"ERROR: input_dir is not a directory: {input_dir}", file=sys.stderr)
        return 2

    print(f"rewrite_comma")
    return do_rewrite(input_dir, output_dir, encoding, dry_run, comma_convert)
