"""
Foundry Local LLM client for ContextCraftPro.

Provides a minimal, robust client for Foundry Local's OpenAI-compatible API.
Handles retries, timeouts, and error categorization for reliable LLM operations.
"""

import json
import time
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Callable
from pathlib import Path
import ssl
import re

from core.ccp_logger import CCPLogger
from core.ccp_config import FoundryLocalConfig


@dataclass
class LLMResponse:
    """Response from LLM with metadata."""

    content: str
    model: str
    usage: Dict[str, int]  # tokens used
    latency_ms: int
    retry_count: int
    success: bool
    error_message: Optional[str] = None


class LLMError(Exception):
    """Base class for LLM-related errors."""

    pass


class ConnectionError(LLMError):
    """Cannot connect to Foundry Local."""

    pass


class TimeoutError(LLMError):
    """Request timed out."""

    pass


class InvalidResponseError(LLMError):
    """Response format is invalid."""

    pass


class ModelNotFoundError(LLMError):
    """Requested model not available."""

    pass


class FoundryLocalClient:
    """
    Minimal, robust client for Foundry Local's OpenAI-compatible API.

    Uses only standard library for HTTP requests to minimize dependencies.
    """

    # User-friendly error messages
    ERROR_MESSAGES = {
        "connection_refused": "Cannot connect to Foundry Local. Please ensure it's running: foundry-local serve",
        "timeout": "Request timed out. Try a simpler prompt or increase timeout in config.",
        "invalid_model": "Model '{model}' not found. Check available models: foundry-local list",
        "rate_limit": "Rate limit exceeded. Please wait before retrying.",
        "invalid_response": "Received invalid response from LLM. Check logs for details.",
        "no_content": "LLM returned empty response. Please try again.",
    }

    def __init__(self, config: FoundryLocalConfig, logger: CCPLogger):
        """
        Initialize Foundry Local client.

        Args:
            config: Foundry Local configuration
            logger: Logger for structured logging
        """
        self.endpoint = config.endpoint
        self.model = config.model
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        self.logger = logger

        # Parse endpoint
        self._validate_endpoint()

    def _validate_endpoint(self):
        """Validate and parse the endpoint URL."""
        try:
            parsed = urllib.parse.urlparse(self.endpoint)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid endpoint URL: {self.endpoint}")
        except Exception as e:
            raise LLMError(f"Invalid endpoint configuration: {e}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        feature_context: Optional[str] = None,
    ) -> LLMResponse:
        """
        Send chat completion request with automatic retry and error handling.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            feature_context: Optional feature name for logging

        Returns:
            LLMResponse with content and metadata
        """
        start_time = time.time()

        # Build request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        # Log the call
        self.logger.info(
            "llm_call_start",
            model=self.model,
            temperature=temperature,
            message_count=len(messages),
            feature=feature_context,
        )

        # Try with retries
        retry_count = 0
        last_error = None

        while retry_count <= self.max_retries:
            try:
                response = self._make_request(payload, retry_count)

                # Parse response
                parsed_response = self._parse_response(response)

                # Calculate metrics
                latency_ms = int((time.time() - start_time) * 1000)

                # Log success
                self.logger.info(
                    "llm_call_success",
                    model=self.model,
                    latency_ms=latency_ms,
                    retry_count=retry_count,
                    tokens_used=parsed_response.get("usage", {}),
                    feature=feature_context,
                )

                return LLMResponse(
                    content=parsed_response["content"],
                    model=parsed_response.get("model", self.model),
                    usage=parsed_response.get("usage", {}),
                    latency_ms=latency_ms,
                    retry_count=retry_count,
                    success=True,
                )

            except (ConnectionError, TimeoutError) as e:
                # Retryable errors
                last_error = e
                retry_count += 1
                if retry_count <= self.max_retries:
                    delay = self._get_retry_delay(retry_count)
                    self.logger.warning(
                        f"Retrying after {delay}s (attempt {retry_count}/{self.max_retries})",
                        error=str(e),
                    )
                    time.sleep(delay)

            except (InvalidResponseError, ModelNotFoundError) as e:
                # Non-retryable errors
                self.logger.error(
                    "llm_call_failed",
                    error_type=type(e).__name__,
                    error_message=str(e),
                    retry_count=retry_count,
                    feature=feature_context,
                )

                return LLMResponse(
                    content="",
                    model=self.model,
                    usage={},
                    latency_ms=int((time.time() - start_time) * 1000),
                    retry_count=retry_count,
                    success=False,
                    error_message=str(e),
                )

        # Max retries exceeded
        error_msg = f"Max retries exceeded. Last error: {last_error}"
        self.logger.error(
            "llm_call_max_retries",
            max_retries=self.max_retries,
            last_error=str(last_error),
            feature=feature_context,
        )

        return LLMResponse(
            content="",
            model=self.model,
            usage={},
            latency_ms=int((time.time() - start_time) * 1000),
            retry_count=retry_count,
            success=False,
            error_message=error_msg,
        )

    def _make_request(self, payload: Dict[str, Any], retry_count: int) -> str:
        """
        Make HTTP request to Foundry Local.

        Args:
            payload: Request payload
            retry_count: Current retry attempt number

        Returns:
            Response body as string

        Raises:
            ConnectionError: Cannot connect to endpoint
            TimeoutError: Request timed out
            InvalidResponseError: Invalid HTTP response
        """
        # Prepare request
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            # Make request with timeout
            response = urllib.request.urlopen(req, timeout=self.timeout)

            # Read response
            response_data = response.read().decode("utf-8")

            if response.getcode() != 200:
                raise InvalidResponseError(
                    f"Unexpected status code: {response.getcode()}"
                )

            return response_data

        except urllib.error.URLError as e:
            if isinstance(e.reason, ConnectionRefusedError):
                raise ConnectionError(self.ERROR_MESSAGES["connection_refused"])
            elif isinstance(e.reason, TimeoutError):
                raise TimeoutError(self.ERROR_MESSAGES["timeout"])
            else:
                raise ConnectionError(f"Connection error: {e.reason}")

        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ModelNotFoundError(
                    self.ERROR_MESSAGES["invalid_model"].format(model=self.model)
                )
            elif e.code == 429:
                raise ConnectionError(self.ERROR_MESSAGES["rate_limit"])
            else:
                # Try to read error message
                try:
                    error_body = e.read().decode("utf-8")
                    error_data = json.loads(error_body)
                    error_msg = error_data.get("error", {}).get("message", str(e))
                except:
                    error_msg = f"HTTP {e.code}: {e.reason}"
                raise InvalidResponseError(f"API error: {error_msg}")

        except Exception as e:
            raise InvalidResponseError(f"Request failed: {e}")

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse and validate LLM response.

        Args:
            response_text: Raw response from API

        Returns:
            Parsed response dictionary

        Raises:
            InvalidResponseError: Response format is invalid
        """
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            self.logger.error("Invalid JSON response", raw_response=response_text[:500])
            raise InvalidResponseError(self.ERROR_MESSAGES["invalid_response"])

        # Extract content based on OpenAI format
        try:
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
            elif "content" in data:
                # Simple format
                content = data["content"]
            else:
                raise KeyError("No content field found")

            if not content:
                raise InvalidResponseError(self.ERROR_MESSAGES["no_content"])

            return {
                "content": content,
                "model": data.get("model", self.model),
                "usage": data.get("usage", {}),
            }

        except KeyError as e:
            self.logger.error(
                "Response missing expected fields", available_keys=list(data.keys())
            )
            raise InvalidResponseError(f"Response missing field: {e}")

    def _get_retry_delay(self, retry_count: int) -> float:
        """
        Calculate retry delay with exponential backoff.

        Args:
            retry_count: Current retry attempt (1-based)

        Returns:
            Delay in seconds
        """
        initial_delay = 1.0
        backoff_factor = 2.0
        max_delay = 30.0

        delay = initial_delay * (backoff_factor ** (retry_count - 1))
        return min(delay, max_delay)

    def test_connection(self) -> bool:
        """
        Test if Foundry Local is accessible.

        Returns:
            True if connection successful, False otherwise
        """
        test_messages = [{"role": "user", "content": "Hello"}]

        response = self.chat_completion(
            messages=test_messages, max_tokens=10, temperature=0
        )

        return response.success


class ContextManager:
    """
    Manages context size for LLM calls.

    Helps fit context within token limits and prioritize important information.
    """

    MAX_CONTEXT_TOKENS = 8000  # Conservative limit for most models

    def __init__(self, logger: CCPLogger):
        self.logger = logger

    def prepare_context(
        self, required: List[Dict[str, Any]], optional: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Fit context within token limits.

        Args:
            required: Context blocks that must be included
            optional: Context blocks that can be trimmed

        Returns:
            List of context blocks that fit within limits
        """
        result = []
        total_tokens = 0

        # Always include required context
        for block in required:
            tokens = self.estimate_tokens(block.get("content", ""))
            if total_tokens + tokens > self.MAX_CONTEXT_TOKENS:
                self.logger.warning(
                    "Required context exceeds token limit",
                    required_tokens=total_tokens + tokens,
                    max_tokens=self.MAX_CONTEXT_TOKENS,
                )
            result.append(block)
            total_tokens += tokens

        # Add optional context if space available
        for block in optional:
            tokens = self.estimate_tokens(block.get("content", ""))
            if total_tokens + tokens <= self.MAX_CONTEXT_TOKENS:
                result.append(block)
                total_tokens += tokens
            else:
                self.logger.debug(
                    "Skipping optional context due to token limit",
                    block_name=block.get("name", "unknown"),
                )

        self.logger.debug(
            "Context prepared", total_tokens=total_tokens, block_count=len(result)
        )

        return result

    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (1 token ≈ 4 characters).

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count
        """
        # More accurate estimation based on common patterns
        # Adjust for whitespace and punctuation
        chars = len(text)
        words = len(text.split())

        # Average of character and word-based estimates
        char_estimate = chars / 4
        word_estimate = words * 1.3

        return int((char_estimate + word_estimate) / 2)

    def detect_secrets(self, text: str) -> List[str]:
        """
        Detect potential secrets in text.

        Args:
            text: Text to scan for secrets

        Returns:
            List of potential secret patterns found
        """
        patterns = [
            (r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9\-_]{20,}', "API key"),
            (r'token\s*[:=]\s*["\']?[a-zA-Z0-9\-_]{20,}', "Token"),
            (r'password\s*[:=]\s*["\']?[^\s"\']{8,}', "Password"),
            (r"[a-zA-Z0-9\-_]{40}", "Possible SHA token"),
            (r"-----BEGIN [A-Z]+ PRIVATE KEY-----", "Private key"),
        ]

        found = []
        for pattern, name in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(name)

        if found:
            self.logger.warning("Potential secrets detected in context", types=found)

        return found
