# Contributing to Quantum Fraud Detection System

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Getting Started

1. **Fork the Repository**
   ```bash
   # Click the 'Fork' button on GitHub
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/quantum_hackathon.git
   cd quantum_hackathon
   ```

2. **Set Up Development Environment**
   ```bash
   # Python environment
   py -3.13 -m venv venv-new
   .\venv-new\Scripts\activate  # Windows
   # source venv-new/bin/activate  # Unix/Linux/Mac
   pip install -r requirements.txt
   
   # Java environment (automatic via build scripts)
   .\build.cmd clean install
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Python Code

- **Style**: Follow PEP 8 guidelines
- **Formatting**: Use Black for code formatting
  ```bash
  black model/ tests/
  ```
- **Linting**: Use Flake8 to check code quality
  ```bash
  flake8 model/ tests/
  ```
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Use Google-style docstrings

Example:
```python
def process_transaction(transaction: dict, model: str = "random_forest") -> float:
    """
    Process a transaction and return fraud probability.
    
    Args:
        transaction: Dictionary containing transaction data
        model: Model to use for prediction (default: "random_forest")
        
    Returns:
        Fraud probability between 0 and 1
        
    Raises:
        ValueError: If transaction data is invalid
    """
    # Implementation
    pass
```

### Java Code

- **Style**: Follow standard Java conventions
- **Testing**: Write JUnit tests for all new features
- **Logging**: Use SLF4J for logging
- **Documentation**: Use Javadoc for public methods

Example:
```java
/**
 * Detects fraud in a list of transactions.
 *
 * @param transactions List of transactions to analyze
 * @return List of fraud predictions
 * @throws RuntimeException if processing fails
 */
public List<FraudPrediction> detectFraud(List<Transaction> transactions) {
    // Implementation
}
```

### Testing

**Python Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=model --cov-report=html

# Run specific test
pytest tests/test_fraud_detection.py -v
```

**Java Tests:**
```bash
.\build.cmd test  # Windows
./build.sh test   # Unix/Linux/Mac
```

### Commit Messages

Use clear, descriptive commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(model): Add quantum circuit optimization

Implemented circuit depth reduction algorithm that decreases
quantum gate count by 30% while maintaining accuracy.

Closes #123
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings/comments
   - Update QCENTROID_SETUP.md if quantum features are affected

2. **Run Tests**
   ```bash
   # Python
   pytest --cov=model
   
   # Java
   .\build.cmd clean test
   ```

3. **Code Quality Checks**
   ```bash
   black model/ tests/
   flake8 model/ tests/
   ```

4. **Create Pull Request**
   - Push your branch to your fork
   - Open a PR against the `main` branch
   - Fill in the PR template with:
     - Description of changes
     - Related issues
     - Testing performed
     - Screenshots (if UI changes)

5. **Address Review Comments**
   - Respond to feedback
   - Make requested changes
   - Push updates to your branch

## Code Review Guidelines

Reviewers should check for:
- Code follows project conventions
- Tests are included and passing
- Documentation is updated
- No security vulnerabilities
- Performance considerations
- Quantum circuit optimization (if applicable)

## Areas for Contribution

### High Priority
- [ ] Implement additional quantum algorithms
- [ ] Optimize quantum circuit depth
- [ ] Add more comprehensive tests
- [ ] Improve error handling
- [ ] Add API rate limiting
- [ ] Create deployment documentation

### Medium Priority
- [ ] Add more visualization tools
- [ ] Implement model comparison dashboard
- [ ] Add configuration validation
- [ ] Improve logging
- [ ] Add monitoring/metrics

### Good First Issues
- [ ] Fix typos in documentation
- [ ] Add code comments
- [ ] Improve error messages
- [ ] Add unit tests for existing code
- [ ] Update dependencies

## Questions?

- Open an issue for bugs or feature requests
- Tag questions with `question` label
- For QCentroid integration, refer to [QCENTROID_SETUP.md](QCENTROID_SETUP.md)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in the project README. Thank you for helping improve this project!
