# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and how is it useful?

Static code analysis examines source code without executing the program. It can identify potential bugs, insecure coding patterns, maintainability problems, and style violations early in development. This helps developers improve reliability and makes code easier to review and maintain.

## 2. What did Pylint, Bandit, and Flake8 each help identify?

Pylint checks general Python code quality, including naming, documentation, unused or problematic code, and other programming practices. Bandit checks Python code for common security risks. Flake8 checks style and formatting issues, including many PEP 8 violations. Using all three provides complementary views of the same program.

## 3. Which issues were fixed, and why were those fixes important?

The changes addressed the mutable default argument, overly broad exception handling, invalid seat input, file resource management, overly permissive file permissions, the MD5 ticket-code hash, function naming, and unconditional execution at import time. These changes improve correctness, security, readability, and testability. The actual final findings should be confirmed against the generated tool reports.

## 4. What did you learn, and what are the limitations of static analysis?

I learned that static analysis can reveal problems that may not be obvious during ordinary use, and that different tools focus on different categories of issues. Static analysis does not prove that a program is correct and may produce warnings that require human judgment. It should be combined with functional tests, code review, and testing of realistic and invalid inputs.
