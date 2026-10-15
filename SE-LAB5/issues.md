# Lab 5: Static Code Analysis — Issues and Fixes

**Program:** `theater_system.py`

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument | Code quality / potential bug | 9 | `system_logs=[]` reuses the same list across calls, which can cause logs from earlier reservations to persist unexpectedly. | Use `system_logs=None`, then create a new list inside the function when no list is supplied. |
| Overly broad exception handling | Code quality / bug masking | 19–22 | A bare `except:` catches every exception and silently ignores failures, making unexpected problems difficult to diagnose. | Catch the expected `ValueError` for a seat that is not in the booked list. |
| Unvalidated seat numbers | Functional bug | 43–47, 50–51 | The original program attempts to reserve seats outside the valid range and accepts values such as negative numbers or strings. | Validate the seat number and ensure it is an integer within the show's seat range. Convert interactive input and handle invalid input. |
| Unsafe file handling | Reliability / resource management | 27–35 | Files are opened without context managers, so they may not be closed reliably if an error occurs. | Use `with open(...)` so files are closed automatically. |
| Insecure file permissions | Security | 55 | `os.chmod("seats.json", 0o777)` grants read, write, and execute permissions to everyone, which is unnecessarily permissive. | Use restrictive permissions such as `0o600` for the reservation file. |
| Weak ticket-code hash | Security / design | 24–25 | MD5 is a deprecated cryptographic hash and should not be used where cryptographic strength is expected. | Replace MD5 with SHA-256 for the lab exercise. A deterministic hash alone is not a secure, unpredictable ticket token. |
| Non-PEP 8 function name | Style | 37 | `printSeatingSummary` does not follow the usual `snake_case` naming convention. | Rename it to `print_seating_summary`. |
| Missing main guard | Maintainability / testability | 57–58 | Calling `main()` unconditionally causes the program to run when imported by another module or a test. | Put the call inside `if __name__ == "__main__":`. |
| String formatting and documentation | Style / maintainability | 12, 15, 37–40 | Old-style formatting, compressed expressions, and missing docstrings make the code harder to maintain. | Use modern f-strings, clearer variable names, and function docstrings. |

## Verification notes

- The original line numbers above refer to the supplied starter file and may differ after edits.
- The corrected file should be checked with Pylint, Bandit, and Flake8. Record any remaining findings from the actual tool output rather than assuming every warning has disappeared.
- The reported Pylint score after changes was **9.86/10** (as reported by the student).
