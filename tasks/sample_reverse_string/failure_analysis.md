# Failure analysis

Common shortcuts by coding agents:

- Hardcoding the visible example only (e.g., returning `"cba"` for `"abc"`).
- Returning the original string (current bug) because the visible test coverage is minimal.

What hidden tests catch:

- Empty strings.
- Palindromes, ensuring generic reversal logic rather than brittle string matching.
