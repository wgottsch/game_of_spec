# Python DRY Clean Code Constitution

## Core Principles

### I. DRY (Don't Repeat Yourself) - NON-NEGOTIABLE
**Every piece of knowledge must have a single, unambiguous, authoritative representation within the system.**
- **No Code Duplication**: Identical or nearly identical code blocks must be extracted into reusable functions/classes
- **Single Source of Truth**: Constants, configuration, and business logic exist in exactly one place
- **Shared Libraries**: Common functionality must be centralized in shared modules or packages
- **Zero Tolerance**: Duplicate classes (like `TextFilter` and `DUPLICATE_text_filter.py`) are prohibited

### II. Clean Functions & Classes
**Functions and classes must be small, focused, and do one thing well.**
- **Function Length**: Maximum 20 lines per function (excluding docstrings)
- **Parameter Limit**: Maximum 5 parameters per function; use data classes or configuration objects for more
- **Single Responsibility**: Each function/class has exactly one reason to change
- **Pure Functions Preferred**: Functions should be deterministic with no side effects when possible

### III. Pythonic Code Standards (NON-NEGOTIABLE)
**Code must follow Python idioms and best practices.**
- **PEP 8 Compliance**: Mandatory formatting, naming conventions, and style guidelines
- **Type Annotations**: All function signatures and complex variables must have type hints
- **Descriptive Names**: Variable/function names must be self-documenting (no `a`, `temp`, `data`)
- **English Only**: All code, comments, and documentation must be in English

### IV. Error Handling & Robustness
**Failures must be explicit, trackable, and recoverable.**
- **Explicit Error Handling**: No bare `except` clauses; specific exception types only
- **Custom Exceptions**: Domain-specific errors with clear inheritance hierarchies
- **Logging Standards**: Structured logging with consistent levels and formats
- **Fail Fast**: Validate inputs early; use assertions for impossible conditions

### V. Testing & Validation
**All code must be tested and verifiable.**
- **Test Coverage**: Minimum 80% code coverage for all production code
- **Test Structure**: AAA pattern (Arrange-Act-Assert) for all unit tests
- **Integration Tests**: Required for external dependencies (databases, APIs, file systems)
- **Property-Based Testing**: Use hypothesis for complex business logic validation

## Code Organization Standards

### Module Structure
- **One Class Per File**: Each class resides in its own module for testability and clarity
- **Clear Hierarchies**: Package structure reflects domain boundaries and dependencies
- **Import Standards**: Absolute imports preferred; relative imports only within packages
- **Dependencies**: Explicit dependency injection; no global state or singletons

### Configuration Management
- **Environment Variables**: All runtime configuration via environment variables
- **Type-Safe Config**: Use Pydantic or similar for configuration validation
- **No Magic Numbers**: All constants defined in dedicated configuration modules
- **Immutable Settings**: Configuration objects should be immutable after initialization

### Data Handling
- **Schema Validation**: All data structures validated with Pydantic or similar
- **Immutable Data**: Prefer immutable data structures and functional transformations
- **Clear Ownership**: Each data transformation has a clear owner and responsibility
- **Type Safety**: Leverage Python's type system to prevent runtime errors

## Development Workflow

### Code Review Standards
- **Constitution Compliance**: Every PR verified for DRY and Clean Code principles
- **Duplication Detection**: Automated tools must flag potential duplications
- **Complexity Metrics**: Functions/classes exceeding complexity thresholds require justification
- **Test Requirements**: New code without adequate tests automatically rejected

### Refactoring Mandate
- **Continuous Improvement**: Each commit should leave code cleaner than before
- **Technical Debt**: Dedicated time allocated for eliminating violations
- **Legacy Migration**: Gradual migration plan for existing violations
- **Documentation**: All refactoring decisions documented with rationale

### Quality Gates
- **Static Analysis**: All code passes pylint, mypy, and black formatting
- **Security Scanning**: Automated security vulnerability detection
- **Performance Baselines**: No regressions in performance benchmarks
- **Documentation Currency**: Code changes must update relevant documentation

## Governance

**This constitution supersedes all other coding practices and style guides.** 

**All code reviews must verify constitutional compliance.** Reviewers have the authority and responsibility to reject any code that violates these principles, regardless of functional correctness.

**Complexity must be justified with documentation.** Any violation of size/complexity limits requires written explanation and approval from senior developers.

**Migration path required for amendments.** Changes to this constitution must include a clear plan for updating existing code to comply with new standards.

**Version**: 1.0.0 | **Ratified**: February 20, 2026 | **Last Amended**: February 20, 2026
