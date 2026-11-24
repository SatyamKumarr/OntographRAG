# CHANGELOG
[Configuration Updates]

**Added**
- Added OLLAMA_THINK=false to control thinking-mode behaviour for supported Ollama models.
- Added OLLAMA_NUM_CTX=4096 to configure the Ollama model context window.
- Added OLLAMA_NUM_PREDICT=768 to configure the maximum number of tokens generated per prediction.
- Added explicit error messages listing all supported LLM providers when an unsupported provider is requested.
- Added warning logs to identify embedding initialization failures and fallback attempts.
- Added get_llm_provider as a backward-compatible alias for get_provider.

**Changed**
- Increased LLM_TIMEOUT_SECONDS from 120 to 3000 seconds to accommodate longer-running LLM inference and API requests.
- Changed `0.0.0.0` to `127.0.0.1` for the serve function in `ontographrag/cli.py` and `ontographrag/app/app.py`
- Changed value of chunk_size: int = 1000, and chunk_overlap: int = 150.
- Refactored generate_knowledge_graph() by removing redundant commented-out implementation blocks and simplifying the extraction workflow.
    - Simplified per-chunk LLM extraction by removing nested exception handling around _extract_entities_and_relationships_with_llm().
    - Replaced verbose exception diagnostics and traceback logging with streamlined chunk-level error logging.
    - Removed redundant intermediate logging statements for LLM provider details, model information, extraction input length, and raw extraction results.
    - Removed explicit Neo4j persistence start and completion logging while retaining the persistence operation.
- Updated get_provider() to normalize provider names by trimming whitespace and converting them to lowercase.
    - Refactored provider lookup and initialization for improved readability and maintainability.
    - Updated unsupported-provider validation to provide more informative error messages.
- Changed get_embedding_method() to support automatic fallback from the configured embedding provider to OpenAI.
    - Updated embedding initialization to return the actual provider name associated with the successfully initialized embedding model.
- Increased the default LLM_TIMEOUT_SECONDS configuration from 300 to 3000 seconds. Changed LLM timeout configuration to use floating-point conversion through float(os.getenv(...)), allowing fractional timeout values.

**Removed**
- Removed redundant commented-out exception-handling code.
- Removed extensive diagnostic logging from the individual LLM extraction stage.

**Fixed**
- Previously, complete chunk extraction failure was logged but did not prevent the method from continuing to construct and return a knowledge graph. Now, when all chunks fail (processed_chunks == 0 and failed_chunks > 0), the method raises a RuntimeError with information about the number of failed chunks and a recommendation to check LLM connectivity and rate limits.
