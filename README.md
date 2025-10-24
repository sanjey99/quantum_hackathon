# Quantum Fraud Detection System

A fraud detection system using quantum computing via QCentroid and machine learning, developed during a 36-hour hackathon.

## Project Structure

```
quantum_hackathon/
├── data/           # Dataset storage
├── model/          # Python ML code and notebooks
├── app/            # Java application
└── requirements.txt # Python dependencies
```

## Setup Instructions

### Python Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Java Environment Setup

1. Ensure you have JDK 11+ installed
2. Install Maven if not already installed
3. Build the Java application:
```bash
cd app
mvn clean install
```

## Development Workflow

1. Data Scientists:
   - Work in the `model/` directory
   - Use Jupyter notebooks for data exploration
   - Develop ML models using QCentroid's quantum computing capabilities

2. Backend Engineers:
   - Work in the `app/` directory
   - Run the Spring Boot application using:
   ```bash
   cd app
   mvn spring-boot:run
   ```

3. Testing:
   - Python tests can be run using pytest
   - Java tests can be run using Maven

## Team Members

- Member 1: Data Scientist (Python/ML)
- Member 2: Backend/Integration Engineer (Java)
- Member 3: Support Developer & Integrator

## Technology Stack

- Python for ML/Model Development
  - Pandas, Scikit-learn for classical ML
  - QCentroid for quantum computing
  - Jupyter for interactive development

- Java Spring Boot for Backend
  - REST API for model integration
  - Maven for dependency management

## Project Goals

Build a fraud detection system that:
1. Processes transaction data
2. Uses quantum computing for enhanced pattern recognition
3. Provides real-time fraud detection via API
4. Demonstrates improved accuracy over classical methods