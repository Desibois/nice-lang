#!/usr/bin/env python3
import sys
from nice.compiler import main  # Adjust this if your main compiler function is elsewhere

def run_compiler():
    if len(sys.argv) < 2:
        print("Usage: nice <file.nc>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        main(file_path)  # Call your compiler's main function with the file path
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_compiler()
