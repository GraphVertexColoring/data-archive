import os
import csv

def read_solution_file(filename):
    with open(filename, 'r') as file:
        return len(set(map(int, [line.split()[0] for line in file])))

def load_best_solutions():
    best_solutions = {}
    if not os.path.exists("../../coloring/Resources/best.csv"):
        return best_solutions
    
    with open("../../coloring/Resources/best.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instance = row['Instance']
            best = int(row['best'])
            best_solutions[instance] = best
    return best_solutions

def update_best_solutions():
    best_solutions = load_best_solutions()
    algos = {}

    for root, _, files in os.walk("../../Algos"):
        algorithm = os.path.basename(root)
        for file in files:
            if file.endswith(".sol"):
                solution_file = os.path.join(root, file)
                instance_name, _ = os.path.splitext(file)
                instance = instance_name + ".col"

                new_bound = read_solution_file(solution_file)
                if new_bound < best_solutions.get(instance, float('inf')):
                    best_solutions[instance] = new_bound
                    algos[instance] = algorithm
    
    with open("../../coloring/Resources/best.csv", "w", newline='') as csvfile:
        fieldnames = ['Instance', 'best', 'algorithm']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for instance, best in best_solutions.items():
            algorithm = algos.get(instance, "Unknown")
            writer.writerow({'Instance': instance, 'best': best, 'algorithm': algorithm})

if __name__ == "__main__":
    update_best_solutions()
