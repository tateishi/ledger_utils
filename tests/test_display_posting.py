import pytest
from ledger_utils import models
from ledger_utils.format import display


@pytest.mark.parametrize(
    "token, expected",
    [
        (
            models.Posting(
                account="資産:現金:財布",
            ),
            {
                "text": "    資産:現金:財布",
            },
        ),
        (
            models.Posting(
                account="支出:食費:食料品",
                amount="4276",
            ),
            {
                "text": "    支出:食費:食料品                            4276",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック",
                amount="-660",
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                -660",
            },
        ),
        (
            models.Posting(
                account="収入:投資収入:受取利息",
                amount="-55.26",
                commodity_post="AUD",
            ),
            {
                "text": "    収入:投資収入:受取利息                       -55.26 AUD",
            },
        ),
        (
            models.Posting(
                account="収入:投資収入:受取利息",
                amount="-55.00",
                commodity_post="AUD",
            ),
            {
                "text": "    収入:投資収入:受取利息                       -55.00 AUD",
            },
        ),
        (
            models.Posting(
                account="収入:投資収入:受取利息",
                amount="-55",
                commodity_post="AUD",
            ),
            {
                "text": "    収入:投資収入:受取利息                       -55.00 AUD",
            },
        ),
        (
            models.Posting(
                account="収入:投資収入:受取利息",
                commodity_pre="AUD",
                amount="-55.26",
            ),
            {
                "text": "    収入:投資収入:受取利息                   AUD -55.26",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック", amount="-660", comment="test"
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                -660  ; test",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック",
                amount="-660",
                tags=[models.Tag(tag="a"), models.Tag(tag="b")],
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                -660  ; :a:b:",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック",
                amount="-660",
                meta=models.Meta(name="key", value="value"),
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                -660  ; key: value",
            },
        ),
        (
            models.Posting(account="収入:雑収入:キャッシュバック", comment="test"),
            {
                "text": "    収入:雑収入:キャッシュバック                      ; test",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック",
                tags=[models.Tag(tag="a"), models.Tag(tag="b")],
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                      ; :a:b:",
            },
        ),
        (
            models.Posting(
                account="収入:雑収入:キャッシュバック",
                meta=models.Meta(name="key", value="value"),
            ),
            {
                "text": "    収入:雑収入:キャッシュバック                      ; key: value",
            },
        ),
    ],
)
def test_display(token, expected):
    text = display.display_posting(token)

    if "text" in expected:
        assert text == expected["text"]
