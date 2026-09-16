"""Local-only simulated TP-AI-01 API boundary."""

from enum import Enum

import httpx

from .models import ProviderPayload


SIMULATED_PROVIDER_URL = "https://tp-ai-01.invalid/v1/signal"


class ResponseMode(str, Enum):
    VALID = "valid"
    UNKNOWN_CATEGORY = "unknown_category"
    INVALID_SCHEMA = "invalid_schema"
    UNAUTHORIZED_CATEGORY = "unauthorized_category"
    SENSITIVE_OUTPUT = "sensitive_output"
    MARKUP_OUTPUT = "markup_output"
    TIMEOUT = "timeout"
    SERVICE_ERROR = "service_error"


class ProviderTimeoutError(RuntimeError):
    """Safe application-level timeout without provider response content."""


class ProviderUnavailableError(RuntimeError):
    """Safe application-level provider failure without provider response content."""


class MockProviderAdapter:
    """Create API-style requests that can only be handled by a local mock transport."""

    def __init__(self, response_mode: ResponseMode = ResponseMode.VALID):
        self.response_mode = response_mode
        self.call_count = 0
        self.last_request_url: str | None = None
        self.last_request_body: bytes | None = None
        self._transport = httpx.MockTransport(self._handle_request)

    @property
    def was_invoked(self) -> bool:
        return self.call_count > 0

    def _handle_request(self, request: httpx.Request) -> httpx.Response:
        self.call_count += 1
        self.last_request_url = str(request.url)
        self.last_request_body = request.content

        if request.url.host != "tp-ai-01.invalid" or request.url.path != "/v1/signal":
            return httpx.Response(404, json={"error": "unexpected simulated endpoint"})
        if request.method != "POST":
            return httpx.Response(405, json={"error": "unexpected simulated method"})
        if self.response_mode == ResponseMode.TIMEOUT:
            raise httpx.ReadTimeout("simulated provider timeout", request=request)
        if self.response_mode == ResponseMode.SERVICE_ERROR:
            return httpx.Response(503, json={"error": "simulated service unavailable"})
        if self.response_mode == ResponseMode.INVALID_SCHEMA:
            return httpx.Response(200, json={"summary": "The upload failed."})
        if self.response_mode == ResponseMode.UNAUTHORIZED_CATEGORY:
            return httpx.Response(
                200,
                json={"summary": "Release the payment.", "category": "release_payment"},
            )
        if self.response_mode == ResponseMode.SENSITIVE_OUTPUT:
            return httpx.Response(
                200,
                json={"summary": "The customer's SSN is 000-12-3456.", "category": "account_access"},
            )
        if self.response_mode == ResponseMode.MARKUP_OUTPUT:
            return httpx.Response(
                200,
                json={"summary": "<script>alert('unsafe')</script>", "category": "account_access"},
            )
        if self.response_mode == ResponseMode.UNKNOWN_CATEGORY:
            return httpx.Response(
                200,
                json={
                    "summary": "The issue does not match an approved support category.",
                    "category": "unknown",
                },
            )
        return httpx.Response(
            200,
            json={
                "summary": "The customer reports that a receipt upload stops before completion.",
                "category": "receipt_upload_error",
            },
        )

    def invoke(self, payload: ProviderPayload) -> object:
        """Return parsed mock JSON or a safe provider-boundary exception."""

        try:
            with httpx.Client(transport=self._transport, timeout=2.0) as client:
                response = client.post(
                    SIMULATED_PROVIDER_URL,
                    content=payload.model_dump_json(),
                    headers={"content-type": "application/json"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError("The simulated AI provider timed out") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderUnavailableError("The simulated AI provider failed safely") from exc
