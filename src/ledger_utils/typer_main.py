import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import typer

from ledger_utils.count import account_count, payee_count, tags_count
from ledger_utils.rewrite import comma_convert, plain_convert

app = typer.Typer()


def iter_files_recursively(root: Path, pattern: str):
    yield from (p for p in root.rglob(pattern) if p.is_file())


def print_result(total: dict[str, int], header: str | None = None):
    if header is not None:
        print(header)
    for key, value in sorted(total.items(), key=lambda x: (x[1], x[0])):
        print(f"{value:5d}  {key}")


def compute_output_path(in_file: Path, in_root: Path, out_root: Path | None) -> Path:
    """
    out_root が None の場合は in_file 自体（上書き）。
    out_root がある場合は in_root からの相対パスを out_root 配下に再現。
    """
    if out_root is None:
        return in_file
    rel = in_file.relative_to(in_root)
    return out_root / rel


def convert_one_file(
    in_file: Path,
    out_file: Path,
    convert: Callable[[str], str],
    encoding: str = "utf-8",
) -> bool:
    """
    1ファイル変換して出力。変更があったら True、無ければ False。
    """
    original = in_file.read_text(encoding=encoding)
    converted = convert(original)

    if converted == original and out_file == in_file:
        # 上書きモードで差分なしなら何もしない
        return False

    # 出力先ディレクトリ作成（必要な場合）
    out_file.parent.mkdir(parents=True, exist_ok=True)
    # 出力（上書き含む）
    out_file.write_text(converted, encoding=encoding)
    return converted != original


def do_rewrite(
    input_dir: Path,
    output_dir: Path | None,
    encoding: str,
    dry_run: bool,
    convert: Callable[[str], str],
) -> int:

    in_root: Path = input_dir
    if not in_root.exists() or not in_root.is_dir():
        print(f"ERROR: input_dir is not a directory: {in_root}", file=sys.stderr)
        return 2

    out_root: Path | None = output_dir
    if out_root is not None and out_root.exists() and not out_root.is_dir():
        print(f"ERROR: output_dir is not a directory: {out_root}", file=sys.stderr)
        return 2

    files = list(iter_files_recursively(in_root, "*.ledger"))
    if not files:
        print("No *.ledger files found.")
        return 0

    changed = 0
    processed = 0

    for f in files:
        processed += 1
        out_path = compute_output_path(f, in_root, out_root)

        if dry_run:
            print(f"[DRY] {f} -> {out_path}")
            continue

        try:
            did_change = convert_one_file(f, out_path, convert, encoding=encoding)
            if did_change:
                changed += 1
                print(f"[OK]  {f} -> {out_path} (changed)")
            else:
                # out_root がある場合は「コピー」になる可能性があるので表示を分ける
                status = "unchanged"
                if out_root is not None and out_path != f:
                    status = "written (no content change)"
                print(f"[OK]  {f} -> {out_path} ({status})")
        except Exception as e:
            print(f"[NG]  {f}: {e}", file=sys.stderr)

    print(f"Processed: {processed}, Changed: {changed}")
    return 0


@app.command()
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


@app.command()
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


@app.command()
def hello():
    print("hello world")


@app.command()
def count_payee(path: Path):
    header = "count  payee"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = payee_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = payee_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")


@app.command()
def count_account(path: Path):
    header = "count  account"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = account_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = account_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")


@app.command()
def count_tags(path: Path):
    header = "count  tags"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = tags_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = tags_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")


def main():
    # typer.run(add)
    app()
