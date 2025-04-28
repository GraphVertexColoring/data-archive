import subprocess
import sys
import argparse
import os
import gzip
import shutil

# Standard unzip method.
def unzip_gz_file(file_path, output_path):
    with gzip.open(file_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Cleanup method for removing files after use
#  is run per iteration to avoid caching to many files
def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

# method that calls the coloring-verifier
def verify(algo_path):
    name    = os.path.basename(algo_path)
    sol_gz  = f"{algo_path}.sol.gz"
    sol     = f"{algo_path}.sol"
    col_gz  = os.path.join("gvc-instances/Instances", f"{name}.col.gz")
    col     = os.path.join("gvc-instances/Instances", f"{name}.col")

    # Unzip
    unzip_gz_file(sol_gz, sol)
    unzip_gz_file(col_gz, col)

    result = subprocess.run([
        "./coloring-verifier",
        "-i", col,
        "-s", sol,
        "-p", "coloring"
    ], capture_output=True, text=True)

    print(f"Return code for {sol}: {result.returncode}")
    if result.returncode != 0:
        print(f"Verification failed for {sol}")
        print(result.stdout)
        cleanup_files(sol,col)
        return False
    
    cleanup_files(sol,col)
    return True
    
def main():
    # add arg here that takes the algorithms path
    parser = argparse.ArgumentParser(description= "Takes a path to a algorithm directory, which contains .sol files and validates the solutions using the instance files and a validator made in c.")
    parser.add_argument('algo_dir', help="Directory containing the files (e.g., Algos/run*/dsatur/)")
    args = parser.parse_args()

    algo_dir = args.algo_dir
    algo_paths = []

    for root, dirs, files in os.walk(algo_dir):
        for file in files:
            if file.endswith('.sol.gz'):
                algo_path = os.path.join(root,file[:-7]) # removes the file ending .sol.gz to get a base name for the file
                algo_paths.append(algo_path)

    if not algo_paths:
        print("No algorithm solutions found")
        sys.exit(1)

    valid = True
    for algo_path in algo_paths:
        if not verify(algo_path):
            valid = False

    if not valid: # if a solution is invalid return 1 for error.
        sys.exit(1)

if __name__=="__main__":
    main()