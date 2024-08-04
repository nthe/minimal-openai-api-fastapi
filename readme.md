**Minimal OpenAI API in FastAPI**

Endpoints:
 - chat completions
 - files (in-memory store)
 - models

Usage:
```sh
uvicorn src.api.server:app --host {host} --port {port}
```

See `src/api/state.py` for setup of dependencies and global (shared) state.
