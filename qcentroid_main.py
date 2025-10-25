"""
QCentroid-compatible entry point for DBS Fraud Detection QSVM
Accepts input data from QCentroid platform
"""
import json
import sys
import numpy as np
from pathlib import Path

def main():
    try:
        print("="*80)
        print("   DBS FRAUD DETECTION - QSVM SOLVER")
        print("   Running on QCentroid Platform")
        print("="*80)
        print()
        
        # QCentroid provides input data via stdin or as arguments
        # Try to read from stdin first
        input_data = None
        if not sys.stdin.isatty():
            try:
                input_data = json.load(sys.stdin)
                print("✓ Received input data from stdin")
            except:
                print("⚠ Failed to parse stdin, using local configuration")
        
        if input_data is None:
            print("⚠ No stdin data, using local dataset")
            # Fallback: use local data
            from quantum_solver import main as run_quantum_solver
            return run_quantum_solver()
        
        # Extract configuration from input
        additional_args = input_data.get('additional_arguments', {})
        dataset_info = input_data.get('dataset_info', {})
        
        print(f"✓ Dataset: {dataset_info.get('name', 'Credit Card Fraud')}")
        print(f"✓ Random state: {additional_args.get('random_state', 42)}")
        print()
        
        # Check if processed data exists locally
        data_path = Path('data/processed')
        if not data_path.exists() or not list(data_path.glob('*.npy')):
            print("⚠ Processed data not found locally")
            print("✓ Preparing to download and process dataset...")
            
            # Download and process data
            try:
                from model.load_kaggle_data import main as load_data
                print("✓ Running data preparation...")
                load_data()
                print("✓ Data preparation complete")
                print()
            except Exception as e:
                print(f"⚠ Data preparation failed: {e}")
                print("✓ Continuing with available data...")
        else:
            print("✓ Using existing processed data")
            print()
        
        # Now run the quantum solver
        print("="*80)
        print("   STARTING QUANTUM SOLVER")
        print("="*80)
        print()
        
        from quantum_solver import main as run_quantum_solver
        result = run_quantum_solver()
        
        # Format output for QCentroid
        output = {
            "status": "success",
            "solver": "DBS Fraud Detection QSVM",
            "result": result,
            "additional_info": {
                "random_state": additional_args.get('random_state', 42),
                "save_results": additional_args.get('save_results', True)
            }
        }
        
        # Return output as JSON
        print()
        print("="*80)
        print("   EXECUTION COMPLETE")
        print("="*80)
        print(json.dumps(output, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error output
        error_output = {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_output, indent=2))
        return 1

if __name__ == '__main__':
    sys.exit(main())
