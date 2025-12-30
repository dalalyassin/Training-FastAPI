from collections.abc import Generator


def stream_tokens(
    tokens: list[str], trace_id: str | None = None
) -> Generator[str, None, None]:
    """
    Simulates token-by-token streaming.
    Each token is sent as a Server-Sent Event (SSE).
    Optionally logs trace info.
    """
    for token in tokens:
        if trace_id:
            print(f"[TRACE {trace_id}] Streaming token: {token}")
        yield f"data: {token}\n\n"
