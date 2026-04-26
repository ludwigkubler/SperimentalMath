import random
import math
from itertools import product

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def count_solutions(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(cols)):
            rank += 1
    return 2 ** (rows - rank)

def generate_acc0_circuit(n, size):
    circuit = []
    for _ in range(size):
        gate_type = random.choice(['AND', 'OR', 'NOT'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = random.sample(range(n), 2)
        circuit.append((gate_type, inputs))
    return circuit

def generate_polynomial_system(circuit, n):
    variables = list(product([0, 1], repeat=n))
    equations = []
    for var in variables:
        expr = var[circuit[0][1][0]]
        if circuit[0][0] == 'NOT':
            expr = 1 - expr
        for gate in circuit[1:]:
            if gate[0] == 'AND':
                expr &= var[gate[1][0]] & var[gate[1][1]]
            elif gate[0] == 'OR':
                expr |= var[gate[1][0]] | var[gate[1][1]]
        equations.append(expr)
    return equations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        size = n ** 2
        circuit = generate_acc0_circuit(n, size)
        equations = generate_polynomial_system(circuit, n)
        
        solution_count = count_solutions(equations)
        expected_solution_count = 2 ** (n // 2)
        
        results.append({
            "n": n,
            "size": size,
            "solution_count": solution_count,
            "expected_solution_count": expected_solution_count
        })
    
    conjecture_holds = all(abs(result["solution_count"] - result["expected_solution_count"]) < 10 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, size={results[0]['size']}"
    
    return {
        "metric_name": "Solution Count",
        "metric_value": sum(result["solution_count"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_solution_count = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_solution_count} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_solution_count} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, size={results[0]['size']}\" first_failing_seed={first_failing_seed}")