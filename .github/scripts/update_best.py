import os
import csv
from datetime import datetime

BEST_CSV = os.path.join("..","..","coloring","Resources","best.csv")
ALGOS_ROOT = os.path.join("..","..","Algos")

def read_solution_file(filename):
    with open(filename, 'r') as file:
        return len(set(map(int, [line.split()[0] for line in file])))

def load_best_solutions():
    best_solutions = {}
    if not os.path.exists(BEST_CSV):
        return best_solutions
    
    with open(BEST_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instance = row['Instance']
            best = int(row['Best'])
            algo = row.get('Algorithm', 'Unknown')
            old_timestamp = row.get('Last Improved', 'Unknown')
            best_solutions[instance] = (best,algo, old_timestamp)
    return best_solutions

def update_best_solutions():
    best_solutions = load_best_solutions()

    for root, _, files in os.walk(ALGOS_ROOT):
        algorithm = os.path.basename(root)
        for file in files:
            if not file.endswith('.sol'):
                continue

            solution_file = os.path.join(root, file)
            instance_name, _ = os.path.splitext(file)
            instance = instance_name + ".col"

            new_bound = read_solution_file(solution_file)
            old_best, old_algo = best_solutions.get(instance, (float('inf'), 'Unknown'))
            # Should only replace if strictly better.
            if new_bound < old_best:
                best_solutions[instance] = (new_bound,algorithm, datetime.now().isoformat())
    
    with open(BEST_CSV, "w", newline='') as csvfile:
        fieldnames = ['Instance', 'Best', 'Algorithm', 'Last Improved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for instance, (best, algo, ts) in sorted(best_solutions.items()):
            writer.writerow({
                'Instance': instance, 
                'Best': best, 
                'Algorithm': algo,
                'Last Improved': ts
            })

if __name__ == "__main__":
    update_best_solutions()
