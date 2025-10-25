#!/usr/bin/env python3
"""
QCentroid Configuration Module

This module provides configuration and connection management for QCentroid's
quantum computing platform. It handles authentication, backend selection,
and job submission.

Includes support for DBS Fraud Detection Challenge API:
https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam
"""

import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class QCentroidConfig:
    """Configuration class for QCentroid connection"""
    
    def __init__(self):
        self.api_key = os.getenv('QCENTROID_API_KEY')
        self.workspace_id = os.getenv('QCENTROID_WORKSPACE_ID')
        self.api_url = os.getenv('QCENTROID_API_URL', 'https://api.qcentroid.com/v1')
        self.backend = os.getenv('QCENTROID_BACKEND', 'simulator')
        self.max_qubits = int(os.getenv('QCENTROID_MAX_QUBITS', '10'))
        self.shots = int(os.getenv('QCENTROID_SHOTS', '1024'))
        
        # Challenge-specific configuration
        self.challenge_api_url = 'https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam'
        self.use_challenge_endpoint = os.getenv('USE_CHALLENGE_ENDPOINT', 'false').lower() == 'true'
        
    def validate(self) -> bool:
        """Validate that required configuration is present"""
        if not self.api_key:
            print("Warning: QCENTROID_API_KEY not set. Some features may not work.")
            return False
        if not self.workspace_id:
            print("Warning: QCENTROID_WORKSPACE_ID not set. Using default workspace.")
        return True
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }


class QCentroidChallengeAPI:
    """
    Client for DBS Fraud Detection Challenge API endpoint.
    
    API Endpoint: https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam
    """
    
    def __init__(self, api_key: str):
        self.api_url = 'https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam'
        self.api_key = api_key
    
    def submit_job(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a job to the challenge API.
        
        Args:
            input_data: Input data following the challenge JSON schema
            
        Returns:
            API response with job ID and status
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=input_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error submitting job to challenge API: {e}")
            return {'error': str(e)}
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a submitted job.
        
        Args:
            job_id: Job ID returned from submit_job
            
        Returns:
            Job status and results
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.api_url}/jobs/{job_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting job status: {e}")
            return {'error': str(e)}


class QCentroidClient:
    """
    Client for interacting with QCentroid's quantum platform.
    
    This is a wrapper/adapter that can work with different quantum backends.
    Currently supports:
    - QCentroid native API (when available)
    - Qiskit (IBM Quantum)
    - PennyLane
    """
    
    def __init__(self, config: Optional[QCentroidConfig] = None):
        self.config = config or QCentroidConfig()
        self.config.validate()
        self._backend = None
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Initialize the quantum backend"""
        try:
            # Try to import qcentroid first
            import qcentroid as qc
            self._backend_type = 'qcentroid'
            self.client = qc.Client(
                api_key=self.config.api_key,
                workspace_id=self.config.workspace_id,
                api_url=self.config.api_url
            )
            print(f"✓ Connected to QCentroid backend: {self.config.backend}")
            
        except ImportError:
            # Fallback to Qiskit
            print("QCentroid not available, using Qiskit simulator as fallback...")
            self._initialize_qiskit_backend()
    
    def _initialize_qiskit_backend(self):
        """Initialize Qiskit as fallback backend"""
        try:
            from qiskit import Aer
            from qiskit.providers.aer import AerSimulator
            
            self._backend_type = 'qiskit'
            
            if self.config.backend == 'simulator':
                self._backend = AerSimulator()
                print(f"✓ Using Qiskit AerSimulator")
            else:
                # For real hardware, would need IBM Quantum credentials
                print("Real quantum hardware requires IBM Quantum account")
                self._backend = AerSimulator()
                
        except ImportError:
            print("Error: Neither QCentroid nor Qiskit available!")
            print("Install with: pip install qiskit qiskit-aer")
            self._backend_type = None
    
    def get_backend(self):
        """Get the quantum backend for circuit execution"""
        if self._backend_type == 'qcentroid':
            return self.client.get_backend(self.config.backend)
        elif self._backend_type == 'qiskit':
            return self._backend
        else:
            raise RuntimeError("No quantum backend available")
    
    def submit_circuit(self, circuit, shots: Optional[int] = None):
        """
        Submit a quantum circuit for execution
        
        Args:
            circuit: Quantum circuit to execute
            shots: Number of times to run the circuit (default from config)
            
        Returns:
            Job object or result depending on backend
        """
        shots = shots or self.config.shots
        
        if self._backend_type == 'qcentroid':
            job = self.client.execute(
                circuit,
                backend=self.config.backend,
                shots=shots
            )
            return job
            
        elif self._backend_type == 'qiskit':
            from qiskit import execute
            job = execute(circuit, self._backend, shots=shots)
            return job
        else:
            raise RuntimeError("No quantum backend available")
    
    def get_results(self, job):
        """
        Get results from a submitted job
        
        Args:
            job: Job object or job ID
            
        Returns:
            Results object
        """
        if self._backend_type == 'qcentroid':
            if isinstance(job, str):
                return self.client.get_job_results(job)
            return job.result()
            
        elif self._backend_type == 'qiskit':
            return job.result()
        else:
            raise RuntimeError("No quantum backend available")
    
    def is_available(self) -> bool:
        """Check if quantum backend is available"""
        return self._backend_type is not None
    
    def get_backend_info(self) -> dict:
        """Get information about the current backend"""
        return {
            'type': self._backend_type,
            'backend': self.config.backend,
            'max_qubits': self.config.max_qubits,
            'shots': self.config.shots,
            'available': self.is_available()
        }


# Global client instance (lazily initialized)
_qcentroid_client = None

def get_qcentroid_client() -> QCentroidClient:
    """Get or create the global QCentroid client instance"""
    global _qcentroid_client
    if _qcentroid_client is None:
        _qcentroid_client = QCentroidClient()
    return _qcentroid_client


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("QCentroid Configuration Test")
    print("=" * 60)
    
    # Test configuration
    config = QCentroidConfig()
    print(f"\nConfiguration:")
    print(f"  API URL: {config.api_url}")
    print(f"  Backend: {config.backend}")
    print(f"  Max Qubits: {config.max_qubits}")
    print(f"  Shots: {config.shots}")
    
    # Test client
    print(f"\nInitializing client...")
    client = get_qcentroid_client()
    
    info = client.get_backend_info()
    print(f"\nBackend Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    if client.is_available():
        print("\n✓ Quantum backend is ready!")
    else:
        print("\n✗ Quantum backend is not available")
        print("  Install dependencies: pip install qiskit qiskit-aer")
