# LLM Integration Architecture for ContextCraftPro

## Overview

This document defines the architecture for integrating Foundry Local (OpenAI-compatible API) into ContextCraftPro. The design prioritizes reliability, security, and maintainability while ensuring all LLM operations are local-only.

## Core Components

### 1. LLM Client Module (`core/ccp_llm.py`)

#### FoundryLocalClient Class

```python
class FoundryLocalClient:
    """
    Minimal, robust client for Foundry Local's OpenAI-compatible API.

    Responsibilities:
    - HTTP communication with Foundry Local endpoint
    - Retry logic with exponential backoff
    - Timeout handling
    - Response validation
    - Error categorization (network, format, content)
    """

    def __init__(self, config: FoundryLocalConfig, logger: CCPLogger):
        self.endpoint = config.endpoint
        self.model = config.model
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        self.logger = logger

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        feature_context: Optional[str] = None
    ) -> LLMResponse:
        """
        Send chat completion request with automatic retry and error handling.
        """
```

#### LLMResponse Dataclass

```python
@dataclass
class LLMResponse:
    content: str
    model: str
    usage: Dict[str, int]  # tokens used
    latency_ms: int
    retry_count: int
    success: bool
    error_message: Optional[str] = None
```

### 2. Prompt Templates Module (`core/ccp_prompts.py`)

#### Design Principles

1. **Structured Prompts**: Use consistent format across all commands
2. **Context Layering**: Build prompts from reusable context blocks
3. **Variable Safety**: Prevent injection through proper escaping
4. **Token Awareness**: Track and limit context size

#### Template Structure

```python
class PromptBuilder:
    """
    Constructs prompts from templates and context.
    """

    def build_new_feature_prompt(
        self,
        user_input: str,
        project_profile: ProjectProfile,
        existing_features: List[str]
    ) -> List[Dict[str, str]]:
        """
        Build prompt for new-feature command.

        Structure:
        1. System prompt with role and constraints
        2. Project context
        3. User's feature description
        4. Expected output format
        """

    def build_generate_prp_prompt(
        self,
        feature_spec: str,
        project_profile: ProjectProfile,
        claude_rules: str,
        examples: List[str],
        docs_context: str
    ) -> List[Dict[str, str]]:
        """
        Build comprehensive PRP generation prompt.

        Context layers:
        1. Project metadata and constraints
        2. Coding rules from claude.md
        3. Feature specification from INITIAL.md
        4. Relevant examples
        5. Documentation pointers
        6. PRP template structure
        """
```

### 3. Error Handling Strategy

#### Error Categories

1. **Network Errors**
   - Connection refused (Foundry Local not running)
   - Timeout (model taking too long)
   - DNS resolution failures
   - Action: Retry with backoff, clear error message to user

2. **API Errors**
   - Invalid API key/auth (if configured)
   - Rate limiting
   - Model not found
   - Action: Log details, suggest configuration check

3. **Content Errors**
   - Invalid response format (not JSON)
   - Missing expected fields
   - Markdown parsing failures
   - Action: Log raw response, use fallback parsing

4. **Semantic Errors**
   - LLM refuses request
   - Output doesn't match expected structure
   - Contains inappropriate content
   - Action: Retry with refined prompt, fallback to manual input

#### Retry Logic

```python
def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 30.0
) -> Any:
    """
    Generic retry wrapper with exponential backoff.

    Retry on:
    - Connection errors
    - Timeout errors
    - 5xx status codes

    Don't retry on:
    - 4xx client errors
    - Validation failures
    - Explicit refusals
    """
```

### 4. Security Considerations

#### Input Sanitization

1. **Path Traversal Prevention**
   - Validate all file paths stay within ContextCraftPro/
   - Reject paths with `..` or absolute paths outside boundary

2. **Secret Detection**
   - Pattern matching for common secret formats
   - Warning when files like `.env`, `credentials.json` detected
   - Option to exclude files from context

3. **Prompt Injection Prevention**
   - Escape user inputs in prompts
   - Use structured message format
   - Clear boundary markers between context types

#### Output Validation

1. **Markdown Validation**
   - Ensure valid markdown structure
   - Prevent script injection in markdown
   - Validate expected sections exist

2. **Command Validation**
   - Never execute commands suggested by LLM
   - Only write to allowed directories
   - Validate YAML/JSON output formats

### 5. Context Management

#### Context Size Limits

```python
class ContextManager:
    """
    Manages context size for LLM calls.
    """

    MAX_CONTEXT_TOKENS = 8000  # Conservative limit

    def prepare_context(
        self,
        required: List[ContextBlock],
        optional: List[ContextBlock]
    ) -> List[ContextBlock]:
        """
        Fit context within token limits.

        Priority order:
        1. System prompt (always included)
        2. User input (always included)
        3. Project profile (usually included)
        4. Feature spec (if relevant)
        5. Examples (trimmed if needed)
        6. Documentation (trimmed if needed)
        """

    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (1 token ≈ 4 chars).
        """
        return len(text) // 4
```

### 6. Response Processing

#### Markdown Extraction

```python
class ResponseProcessor:
    """
    Processes and validates LLM responses.
    """

    def extract_markdown_sections(
        self,
        response: str,
        expected_sections: List[str]
    ) -> Dict[str, str]:
        """
        Extract expected sections from markdown response.
        """

    def validate_prp_structure(self, prp_content: str) -> ValidationResult:
        """
        Ensure PRP has required sections:
        - Context & Assumptions
        - Goals and Non-Goals
        - Ordered Implementation Steps
        - Implementation Checklist
        - Validation Plan
        """

    def format_feature_spec(self, raw_response: str) -> str:
        """
        Convert LLM response into INITIAL.md format.
        """
```

## Command-Specific Flows

### new-feature Command

```
1. Interactive Q&A Phase (no LLM)
   - Collect user inputs via CLI prompts
   - Build feature context

2. Optional LLM Refinement
   - Send Q&A responses to LLM for structuring
   - Request: "Convert these answers into a feature specification"
   - Fallback: Use template if LLM fails

3. Write to INITIAL.md
   - Append or create feature section
   - Preserve user's exact requirements
```

### generate-prp Command

```
1. Context Gathering
   - Load project profile
   - Read claude.md rules
   - Extract feature from INITIAL.md
   - Scan for relevant examples
   - Load documentation index

2. Prompt Construction
   - System: "You are a senior architect creating a PRP"
   - Context: All gathered information
   - Task: "Create a comprehensive PRP following this template..."

3. Response Processing
   - Validate markdown structure
   - Ensure all sections present
   - Extract into PRP template

4. Human Review
   - Display generated PRP
   - Allow editing before saving
   - Write to context/prps/<feature>.md
```

## Implementation Priority

1. **Phase 4a: Core LLM Client**
   - FoundryLocalClient with basic chat_completion
   - Error handling and retry logic
   - Structured logging of all calls

2. **Phase 4b: Prompt Templates**
   - PromptBuilder with template methods
   - Context management utilities
   - Token estimation

3. **Phase 4c: new-feature Command**
   - Interactive Q&A flow
   - Optional LLM enhancement
   - INITIAL.md writing

4. **Phase 5: generate-prp Command**
   - Full context gathering
   - PRP generation and validation
   - Human review flow

## Testing Strategy

### Unit Tests

```python
# test_llm_client.py
def test_retry_on_connection_error():
    """Should retry 3 times on connection refused."""

def test_timeout_handling():
    """Should raise timeout error after configured duration."""

def test_response_validation():
    """Should validate response has required fields."""
```

### Integration Tests

```python
# test_llm_integration.py
@pytest.mark.requires_foundry
def test_generate_prp_full_flow():
    """Test full PRP generation with mock Foundry Local."""
```

### Mock Foundry Local Server

```python
class MockFoundryServer:
    """
    Test server that mimics Foundry Local API.
    Returns canned responses for testing.
    """
```

## Configuration

### Environment Variables

```bash
# Override default Foundry Local settings
export CCP_FOUNDRY_ENDPOINT="http://localhost:11434/v1/chat/completions"
export CCP_FOUNDRY_MODEL="llama2"
export CCP_FOUNDRY_TIMEOUT=60
export CCP_FOUNDRY_MAX_RETRIES=3

# Optional: API key if Foundry requires auth
export CCP_FOUNDRY_API_KEY="optional-key"
```

### contextcraft.yaml

```yaml
foundry_local:
  endpoint: ${CCP_FOUNDRY_ENDPOINT:-http://localhost:11434/v1/chat/completions}
  model: ${CCP_FOUNDRY_MODEL:-gpt-4o-mini}
  timeout: ${CCP_FOUNDRY_TIMEOUT:-30}
  max_retries: ${CCP_FOUNDRY_MAX_RETRIES:-3}

llm_behavior:
  temperature: 0.7
  max_tokens: 4000
  enable_refinement: true  # Use LLM to refine feature specs
  require_confirmation: true  # Always confirm before writing
```

## Error Messages

### User-Friendly Error Messages

```python
ERROR_MESSAGES = {
    "connection_refused": "Cannot connect to Foundry Local. Please ensure it's running: foundry-local serve",
    "timeout": "Request timed out. Try a simpler prompt or increase timeout in config.",
    "invalid_model": "Model '{model}' not found. Check available models: foundry-local list",
    "rate_limit": "Rate limit exceeded. Please wait before retrying.",
    "invalid_response": "Received invalid response from LLM. Check logs for details.",
}
```

## Monitoring and Logging

### Structured Log Events

```python
# Log every LLM call
logger.info(
    "llm_call",
    command="generate-prp",
    feature=feature_slug,
    prompt_tokens=1234,
    response_tokens=567,
    latency_ms=2500,
    success=True,
    model="gpt-4o-mini"
)

# Log errors with context
logger.error(
    "llm_error",
    command="generate-prp",
    error_type="timeout",
    retry_count=3,
    last_attempt_ms=30000
)
```

## Future Enhancements

1. **Streaming Responses**: Support streaming for long generations
2. **Multiple Model Support**: Allow different models for different tasks
3. **Caching**: Cache responses for identical prompts
4. **Prompt Versioning**: Track prompt template versions
5. **Fine-tuning Support**: Instructions for fine-tuning Foundry models

## Conclusion

This architecture provides a robust, secure, and maintainable foundation for LLM integration in ContextCraftPro. The design emphasizes:

- **Reliability** through comprehensive error handling and retry logic
- **Security** through input sanitization and output validation
- **Maintainability** through modular design and clear separation of concerns
- **Testability** through dependency injection and mock servers
- **User Experience** through clear error messages and confirmation flows

The implementation will proceed in phases, with each component thoroughly tested before integration.