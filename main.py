"""
DBS Fraud Detection Challenge - Quantum Solver
Main entry point for quantum fraud detection

This script runs the quantum-based fraud detection solution:
1. Loads preprocessed Kaggle credit card fraud data
2. Trains QSVM with quantum kernels on QCentroid hardware
3. Evaluates performance metrics
4. Saves predictions and results

Uses REAL quantum computing via QCentroid platform.
"""
import sys
import os
from pathlib import Path

# Run quantum solver
if __name__ == '__main__':
    # Import and run the quantum solver
    from quantum_solver import main as run_quantum_solver
    
    try:
        run_quantum_solver()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERROR DURING EXECUTION")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
