# DRY Clean Code Checklist: Python Development

**Purpose**: Pre-commit and code review checklist to ensure compliance with DRY Clean Code Constitution
**Created**: February 20, 2026
**Reference**: [Constitution](constitution.md)

**Note**: This checklist must be completed for all Python code changes before merge.

## DRY (Don't Repeat Yourself) Compliance

- [ ] CHK001 **No Duplicate Code**: Searched codebase for similar logic/functions (use `git grep`, IDE search)
- [ ] CHK002 **Shared Constants**: All constants moved to dedicated configuration modules (no magic numbers)
- [ ] CHK003 **Common Utilities**: Reusable functions extracted to shared libraries/utilities
- [ ] CHK004 **Single Source of Truth**: Business logic exists in exactly one place
- [ ] CHK005 **Copy-Paste Check**: No identical or near-identical code blocks (use diff tools)

## Clean Functions & Classes

- [ ] CHK006 **Function Size**: All functions ≤ 20 lines (excluding docstrings)
- [ ] CHK007 **Parameter Count**: All functions have ≤ 5 parameters (use data classes if more needed)
- [ ] CHK008 **Single Responsibility**: Each function/class does exactly one thing
- [ ] CHK009 **Pure Functions**: Functions are deterministic with minimal side effects
- [ ] CHK010 **Descriptive Names**: All names are self-documenting (no `data`, `temp`, `utils`)

## Pythonic Code Standards

- [ ] CHK011 **PEP 8 Compliance**: Code formatted with `black`, passes `flake8`
- [ ] CHK012 **Type Annotations**: All function signatures and complex variables have type hints
- [ ] CHK013 **English Only**: No German/other language comments or variable names
- [ ] CHK014 **Import Organization**: Imports follow PEP 8 ordering (stdlib, third-party, local)
- [ ] CHK015 **Docstrings**: All public functions/classes have proper docstrings

## Error Handling & Robustness

- [ ] CHK016 **Specific Exceptions**: No bare `except:` clauses (use specific exception types)
- [ ] CHK017 **Custom Exceptions**: Domain-specific errors defined with clear hierarchies
- [ ] CHK018 **Input Validation**: All inputs validated early with clear error messages
- [ ] CHK019 **Logging Standards**: Structured logging with appropriate levels
- [ ] CHK020 **Resource Cleanup**: Proper use of context managers for files/connections

## Testing & Validation

- [ ] CHK021 **Unit Tests**: All new functions have unit tests (AAA pattern)
- [ ] CHK022 **Test Coverage**: Minimum 80% code coverage for changed code
- [ ] CHK023 **Integration Tests**: External dependencies (DB, API, filesystem) tested
- [ ] CHK024 **Edge Cases**: Error conditions and boundary cases tested
- [ ] CHK025 **Mock Usage**: External dependencies properly mocked in unit tests

## Code Organization

- [ ] CHK026 **Module Structure**: One class per file (excluding simple data classes)
- [ ] CHK027 **Package Hierarchy**: Clear domain boundaries in package structure
- [ ] CHK028 **Dependency Direction**: No circular imports or dependencies
- [ ] CHK029 **Configuration**: All config externalized (environment variables, config files)
- [ ] CHK030 **Documentation**: README/docstring updates for API changes

## Performance & Security

- [ ] CHK031 **Performance**: No obvious performance regressions (benchmark if needed)
- [ ] CHK032 **Memory Usage**: Proper resource management (no obvious memory leaks)
- [ ] CHK033 **Security**: No hardcoded secrets or sensitive data
- [ ] CHK034 **Input Sanitization**: User inputs properly validated and sanitized
- [ ] CHK035 **Dependencies**: No unnecessary dependencies added

## Pre-Merge Requirements

- [ ] CHK036 **Static Analysis**: Code passes `pylint`, `mypy`, `bandit` (security)
- [ ] CHK037 **Tests Pass**: All tests pass in CI/CD pipeline
- [ ] CHK038 **Documentation**: Changes documented in appropriate files
- [ ] CHK039 **Breaking Changes**: Breaking changes documented and communicated
- [ ] CHK040 **Constitution Review**: Code reviewer verified constitutional compliance

## Notes

- **Critical Items**: CHK001, CHK003, CHK006, CHK011, CHK021 are mandatory - no exceptions
- **Documentation**: Add findings/exceptions inline with item numbers
- **Tool Integration**: Integrate static analysis tools into CI/CD pipeline
- **Review Process**: Technical lead must approve any constitutional exceptions

**Reviewer Signature**: ___________________ **Date**: ___________

**Developer Certification**: I certify that all applicable checklist items have been completed and this code complies with the DRY Clean Code Constitution.

**Developer Signature**: ___________________ **Date**: ___________