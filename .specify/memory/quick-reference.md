# Speckit DRY Clean Code Quick Reference

## Constitution Framework Overview

This speckit constitution establishes **DRY (Don't Repeat Yourself)** and **Clean Code** principles specifically for Python development. Use these resources together for maximum effectiveness:

### 📋 Documents Created

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [Constitution](constitution.md) | Core principles and governance | Project setup, team onboarding, architectural decisions |
| [Checklist](dry-clean-code-checklist.md) | Pre-commit validation | Before every commit, during code reviews |
| [Implementation Guide](implementation-guide.md) | Practical examples and patterns | Refactoring sessions, learning new patterns |

### 🎯 Quick Start (5 minutes)

1. **Read the Constitution** - Understand the 5 core principles
2. **Use the Checklist** - Validate your code against CHK001-CHK040
3. **Follow Implementation Examples** - Apply patterns from the guide

### ⚠️ Critical Immediate Actions

Based on codebase analysis, address these **NON-NEGOTIABLE** violations immediately:

#### 1. Code Duplication (Principle I Violation)
```bash
# Found duplicate TextFilter classes:
# - src/twins/text_cleaning_job/text_filter.py
# - twins_ui/components/DUPLICATE_text_filter.py

# Action: Consolidate into shared library (see Implementation Guide)
```

#### 2. Function Complexity (Principle II Violation)
```bash
# Functions with >5 parameters or >20 lines need refactoring
# Example: main() function in preprocessing/__main__.py

# Action: Use configuration data classes (see Implementation Guide)
```

#### 3. Missing Type Annotations (Principle III Violation)
```bash
# Add type hints to all function signatures
# Action: Run mypy and fix all type issues
```

### 🔧 Development Workflow

#### Before Writing Code
1. Check if functionality already exists (avoid duplication)
2. Plan function signature with ≤5 parameters
3. Write tests first (TDD approach)

#### Before Committing
1. Run the [checklist](dry-clean-code-checklist.md) (CHK001-CHK040)
2. Ensure all tests pass
3. Verify static analysis tools pass (pylint, mypy, black)

#### During Code Review
1. Reviewer must verify constitutional compliance
2. Focus on principles I-III (DRY, Clean Functions, Pythonic Code)
3. Reject any code violating core principles

### 🛠️ Tools Integration

```bash
# Install development tools
pip install black flake8 pylint mypy bandit pytest pytest-cov

# Pre-commit hooks (see Implementation Guide for full config)
pre-commit install

# Run quality checks
black src/
flake8 src/
mypy src/
pylint src/
bandit -r src/
pytest --cov=src --cov-fail-under=80
```

### 📊 Success Metrics

Track these metrics to measure constitutional compliance:

| Metric | Target | Tool |
|--------|--------|------|
| Code Coverage | >80% | pytest-cov |
| Duplicate Code | 0% | Manual review + tools |
| Type Coverage | >90% | mypy --strict |
| Function Length | ≤20 lines | pylint |
| Cyclomatic Complexity | ≤10 | pylint |

### 🚨 Violation Response

When constitutional violations are found:

1. **Critical Violations** (DRY, Function Size): Stop development, fix immediately
2. **Standard Violations**: Create technical debt ticket, fix within sprint
3. **Minor Violations**: Address in next refactoring session

### 📚 Learning Path

1. **Week 1**: Master DRY principles and eliminate current duplications
2. **Week 2**: Practice clean function design with real examples
3. **Week 3**: Implement comprehensive testing strategy
4. **Week 4**: Apply dependency injection and advanced patterns

### 🤝 Team Adoption

#### For Team Leads
- [ ] Review constitution with team
- [ ] Integrate checklist into code review process  
- [ ] Set up automated quality gates in CI/CD
- [ ] Schedule refactoring sessions for existing violations

#### For Developers
- [ ] Bookmark this quick reference
- [ ] Use checklist for every commit
- [ ] Study implementation guide examples
- [ ] Participate in constitution governance

### 📞 Support and Questions

- **Constitutional Questions**: Review [Constitution](constitution.md) governance section
- **Implementation Help**: Consult [Implementation Guide](implementation-guide.md) examples
- **Technical Issues**: Use [Checklist](dry-clean-code-checklist.md) for debugging

---

**Remember**: The constitution is not just rules—it's a shared commitment to code quality that enables long-term project success. Every line of code either moves us toward or away from these principles.

**Version**: 1.0.0 | **Last Updated**: February 20, 2026