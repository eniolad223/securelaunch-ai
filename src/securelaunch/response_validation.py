"""LindenArc-owned validation of untrusted TP-AI-01 responses."""

import re

from pydantic import ValidationError

from .inspection import inspect_text
from .models import ProviderResponse, SecurityPolicy


MARKUP_PATTERN = re.compile(
    r"<[^>]+>|\[[^\]]+\]\([^\)]+\)|^\s*#{1,6}\s+",
    flags=re.MULTILINE,
)


class ResponseValidationError(RuntimeError):
    """A safe validation failure that excludes untrusted response content."""


def validate_provider_response(raw_response: object, policy: SecurityPolicy) -> ProviderResponse:
    """Return a trusted response only after every LindenArc check passes."""

    try:
        response = ProviderResponse.model_validate(raw_response)
    except ValidationError as exc:
        raise ResponseValidationError("Provider response schema validation failed") from exc

    if not response.summary.strip():
        raise ResponseValidationError("Provider summary was empty")
    if len(response.summary) > policy.maximum_response_characters:
        raise ResponseValidationError("Provider summary exceeded the size limit")
    if response.category not in policy.allowed_categories:
        raise ResponseValidationError("Provider returned an unauthorized category")
    if MARKUP_PATTERN.search(response.summary):
        raise ResponseValidationError("Provider response contained markup-like content")

    inspected = inspect_text(response.summary, policy)
    if inspected.findings or inspected.prompt_manipulation_detected:
        raise ResponseValidationError("Provider response failed sensitive-content inspection")
    return response
