#!/usr/bin/env python3
"""
QCentroid Configuration Module - DBS Fraud Detection Challenge

This module provides configuration and connection management for QCentroid's
quantum computing platform using the DBS Challenge API endpoint.

Challenge API: https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam

IMPORTANT: This uses REAL quantum hardware via QCentroid - no simulator fallback.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import json
import time

# Load environment variables from .env file
load_dotenv()

class QCentroidConfig:
    """Configuration class for QCentroid connection"""
    
    def __init__(self):
        self.api_key = os.getenv('QCENTROID_API_KEY')
        self.workspace_id = os.getenv('QCENTROID_WORKSPACE_ID')
        
        # DBS Challenge API endpoint
        self.challenge_api_url = os.getenv(
            'QCENTROID_CHALLENGE_API',
            'https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam'
        )
        
        self.backend = os.getenv('QCENTROID_BACKEND', 'qcentroid')
        self.max_qubits = int(os.getenv('QCENTROID_MAX_QUBITS', '10'))
        self.shots = int(os.getenv('QCENTROID_SHOTS', '1024'))
        
    def validate(self) -> bool:
        """Validate that required configuration is present"""
        if not self.api_key:
            raise ValueError("QCENTROID_API_KEY not set in .env file. Required for QCentroid platform.")
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
    
    This submits quantum computing jobs directly to QCentroid's challenge platform.
    API Endpoint: https://api.dev.qcentroid.xyz/use-cases/challenge-2-singapore-t4kmam
    """
    
    def __init__(self, config: Optional[QCentroidConfig] = None):
        self.config = config or QCentroidConfig()
        self.config.validate()
        self.api_url = self.config.challenge_api_url
    
    def submit_quantum_job(self, circuit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a quantum circuit job to the challenge API.
        
        Args:
            circuit_data: Dictionary containing:
                - circuit: Quantum circuit definition (QASM or QCentroid format)
                - shots: Number of executions
                - backend: Quantum backend to use
                - parameters: Additional circuit parameters
            
        Returns:
            API response with job ID and status
        """
        headers = self.config.get_headers()
        
        payload = {
            'workspace_id': self.config.workspace_id,
            'backend': self.config.backend,
            'shots': circuit_data.get('shots', self.config.shots),
            'circuit': circuit_data.get('circuit'),
            'parameters': circuit_data.get('parameters', {}),
            'max_qubits': self.config.max_qubits
        }
        
        try:
            print(f"📤 Submitting quantum job to QCentroid Challenge API...")
            print(f"   Endpoint: {self.api_url}")
            print(f"   Backend: {self.config.backend}")
            print(f"   Shots: {payload['shots']}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"✓ Job submitted successfully!")
            print(f"   Job ID: {result.get('job_id', 'N/A')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error submitting job to challenge API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            raise RuntimeError(f"Failed to submit quantum job: {e}")
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a submitted job.
        
        Args:
            job_id: Job ID returned from submit_quantum_job
            
        Returns:
            Job status and results
        """
        headers = self.config.get_headers()
        url = f"{self.api_url}/jobs/{job_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting job status: {e}")
            return {'error': str(e), 'status': 'unknown'}
    
    def wait_for_job(self, job_id: str, max_wait_time: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """
        Wait for a job to complete.
        
        Args:
            job_id: Job ID to wait for
            max_wait_time: Maximum time to wait in seconds (default: 5 minutes)
            poll_interval: Time between status checks in seconds
            
        Returns:
            Final job results
        """
        print(f"⏳ Waiting for job {job_id} to complete...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status = self.get_job_status(job_id)
            
            job_status = status.get('status', 'unknown')
            print(f"   Status: {job_status}")
            
            if job_status in ['completed', 'success', 'finished']:
                print(f"✓ Job completed successfully!")
                return status
            elif job_status in ['failed', 'error', 'cancelled']:
                print(f"❌ Job failed: {status.get('error', 'Unknown error')}")
                return status
            
            time.sleep(poll_interval)
        
        print(f"⚠️  Job timed out after {max_wait_time} seconds")
        return {'status': 'timeout', 'job_id': job_id}


class QCentroidClient:
    """
    High-level client for QCentroid quantum platform.
    
    This client submits quantum circuits to QCentroid's challenge endpoint
    and retrieves results. NO SIMULATOR - uses real quantum hardware.
    """
    
    def __init__(self, config: Optional[QCentroidConfig] = None):
        self.config = config or QCentroidConfig()
        self.config.validate()
        self.challenge_api = QCentroidChallengeAPI(self.config)
        print(f"✓ Connected to QCentroid Challenge Platform")
        print(f"   API: {self.config.challenge_api_url}")
        print(f"   Backend: {self.config.backend}")
    
    def execute_circuit(self, circuit, shots: Optional[int] = None, parameters: Optional[Dict] = None):
        """
        Execute a quantum circuit on QCentroid platform.
        
        Args:
            circuit: Quantum circuit (Qiskit QuantumCircuit object)
            shots: Number of executions
            parameters: Additional parameters
            
        Returns:
            Execution results
        """
        # Convert circuit to QASM or QCentroid format
        try:
            # Try to export as QASM
            circuit_qasm = circuit.qasm()
        except AttributeError:
            # If not a Qiskit circuit, assume it's already in correct format
            circuit_qasm = str(circuit)
        
        circuit_data = {
            'circuit': circuit_qasm,
            'shots': shots or self.config.shots,
            'parameters': parameters or {}
        }
        
        # Submit job
        job_result = self.challenge_api.submit_quantum_job(circuit_data)
        
        # Wait for completion
        job_id = job_result.get('job_id')
        if job_id:
            final_result = self.challenge_api.wait_for_job(job_id)
            return final_result
        
        return job_result
    
    def is_available(self) -> bool:
        """Check if QCentroid backend is available"""
        try:
            self.config.validate()
            return True
        except ValueError:
            return False
    
    def get_backend_info(self) -> dict:
        """Get information about the current backend"""
        return {
            'type': 'qcentroid',
            'backend': self.config.backend,
            'api_url': self.config.challenge_api_url,
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
