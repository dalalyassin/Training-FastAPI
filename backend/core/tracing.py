import uuid
from fastapi import Depends


def create_trace_id() -> str:
    """
    Generates a unique trace ID per request.
    """
    return str(uuid.uuid4())


def get_trace_id(trace_id: str = Depends(create_trace_id)) -> str:
    """
    Dependency that provides a request-scoped trace ID.
    """
    return trace_id
