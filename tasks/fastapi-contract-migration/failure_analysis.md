# Failure analysis: fastapi-contract-migration

## Common failure modes

1. **Fixes only happy path**
   - Agent updates `/ask` success flow but leaves malformed input and model-unavailable branches inconsistent.
   - Hidden tests send malformed input and missing-model cases.

2. **Changes public API unexpectedly**
   - Agent renames fields or drops `metadata` in certain branches.
   - Hidden tests assert stable top-level keys (`answer`, `metadata`).

3. **Swallows all exceptions**
   - Agent catches `Exception` broadly and always returns 200 with vague text.
   - Hidden tests require missing model to return 503 and controlled error behavior.

4. **Hardcodes response for visible test**
   - Agent returns contract only for one specific FEN used by visible tests.
   - Hidden tests use multiple FEN-like inputs and missing-model toggles.
