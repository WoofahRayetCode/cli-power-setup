---
name: headless-test-condenser
description: Test suite output condenser and noise filter for autonomous CLI runs. Strips thousands of lines of passing test output from pytest, cargo test, npm/vitest, and ctest, surfacing only actionable failures, stack traces, and lines to slash context token consumption by up to 95%.
---

# Headless Test Condenser (`headless-test-condenser`)

During autonomous YOLO and background test runs, standard test runners emit thousands of lines of successful status messages (`... ok`, `PASSED`, checkmarks). Passing test logs provide **zero diagnostic value** while consuming massive context window tokens and inflating API billing.

This skill standardizes condensed test invocation patterns that filter green passes and surface **only actionable failures**.

---

## 1. Test Invocation Fast Matrix

When running test suites autonomously, always execute tests using these condensed flags:

| Ecosystem | Standard Noisy Command | Condensed Low-Token Command | Token Reduction |
| :--- | :--- | :--- | :--- |
| **Python / pytest** | `pytest` | `pytest -q --tb=short --no-header` | **~85%** |
| **Rust / cargo** | `cargo test` | `cargo test -q -- --nocapture` | **~75%** |
| **Node / vitest** | `npx vitest run` | `npx vitest run --reporter=basic` | **~80%** |
| **Node / jest** | `npm test` | `npm test -- --silent --reporters=default` | **~80%** |
| **Go** | `go test ./...` | `go test ./... | grep -E "(FAIL|--- FAIL)"` | **~90%** |
| **C / C++ (ctest)** | `ctest -V` | `ctest --output-on-failure` | **~95%** |

---

## 2. Failure Isolation Protocol (Single-Target Re-run)

When an autonomous test run finishes with failing tests:
1. **Never re-run the entire test suite** while diagnosing the failure.
2. Immediately isolate the exact failing module or test case:
   ```bash
   # Pytest: re-run ONLY the failing test
   pytest tests/test_module.py::test_specific_case -v --tb=short

   # Cargo: re-run ONLY the failing test target
   cargo test test_specific_name -- --nocapture

   # Vitest / Jest: re-run ONLY the matching test pattern
   npx vitest run -t "failing test name"
   ```
3. Only after the isolated test passes, perform one final condensed suite run (`pytest -q`) to verify no regressions occurred.

---

## 3. High-Density Failure Reporting

When reporting test results into context, extract only:
- **Test ID:** `test_filename.py::test_case_name`
- **Error Line:** `line 42: AssertionError: expected 200, got 404`
- **Root Failure:** 3-line traceback snippet (omit framework boilerplates).
