import re
from pathlib import Path

COMMENT_RE = re.compile(
    r"""^
    \s*
    ;\s*(?P<comment>.*)$
    """,
    re.VERBOSE,
)


TAG_RE = re.compile(
    r"""
    \s*:(?P<tags>.+):
    """)

def counter(text: str) -> dict[str, int]:
    """
    {TAG, 出現数}の辞書を返す
    """

    count_dict = dict()

    lines = text.splitlines()

    for line in lines:
        m_comment = re.match(COMMENT_RE, line)
        if m_comment is None:
            continue

        comment = m_comment.group("comment")

        print(f"comment=[{comment}]")

        m_tags = re.match(TAG_RE, comment)
        if m_tags is None:
            continue

        tags = m_tags.group("tags")

        print(f"comment=[{comment}], tags=[{tags}]")

    return count_dict


def count(path: Path) -> dict[str, int]:
    """
    ファイル Path に出現する tagの回数を返す
    """

    text = path.read_text()
    return counter(text)
