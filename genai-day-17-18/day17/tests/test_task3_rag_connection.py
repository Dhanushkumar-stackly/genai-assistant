import pytest

from day17_app.rag_client import (
    EmptyTranscriptError,
    ExistingRAGClient,
)


class FakeResponse:

    def raise_for_status(self):
        pass

    def json(self):

        return {
            "answer": (
                "Answer based on document: "
                "Company Leave Policy"
            ),
            "sources": [
                {
                    "document_id": "doc-001",
                    "title": "Company Leave Policy",
                    "score": 1.0,
                }
            ],
        }


class FakeClient:

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        pass

    async def post(
        self,
        url,
        json,
    ):

        assert url.endswith("/ask")

        assert (
            json["question"]
            == "What is the leave policy?"
        )

        return FakeResponse()


@pytest.mark.asyncio
async def test_transcript_is_cleaned_and_sent_to_ask(
    monkeypatch,
):

    import day17_app.rag_client as module

    monkeypatch.setattr(
        module.httpx,
        "AsyncClient",
        lambda timeout: FakeClient(),
    )

    client = ExistingRAGClient(
        base_url="http://existing-rag"
    )

    result = await client.ask(
        "  What   is   the   leave   policy?  "
    )

    assert (
        result.answer
        == "Answer based on document: "
        "Company Leave Policy"
    )

    assert result.sources[0]["title"] == (
        "Company Leave Policy"
    )

    assert result.rag_latency_ms >= 0


def test_empty_transcript_is_rejected():

    client = ExistingRAGClient(
        base_url="http://existing-rag"
    )

    with pytest.raises(
        EmptyTranscriptError
    ):

        import asyncio

        asyncio.run(
            client.ask("   ")
        )


def test_empty_string_transcript_is_rejected():

    client = ExistingRAGClient(
        base_url="http://existing-rag"
    )

    with pytest.raises(
        EmptyTranscriptError
    ):

        import asyncio

        asyncio.run(
            client.ask("")
        )

