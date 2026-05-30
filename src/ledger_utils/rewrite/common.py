from pathlib import Path
from typing import Callable

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
