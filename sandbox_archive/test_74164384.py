import random
import math
import sys
import json
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def cross_correlation_flow_norm(C, T):
    n = len(C)
    norm = 0
    for i in range(n):
        for j in range(i+1, n):
            norm += abs(C[i][j])
    return norm

def communication_complexity_lower_bound(norm):
    # Placeholder function to simulate a lower bound calculation
    return norm ** 0.5

def generate_circuit(n):
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    B = gaussian_elimination(A)
    C = matrix_multiplication(B, B)
    T = [[i == j for i in range(n)] for j in range(n)]
    return C, T

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        C, T = generate_circuit(n)
        k = 2
        lifted_C = matrix_multiplication(C, C)
        lifted_T = [[i == j for i in range(k*n)] for j in range(k*n)]
        
        entropy = cross_correlation_flow_norm(lifted_C, lifted_T)
        communication_complexity = communication_complexity_lower_bound(entropy)
        
        results.append({
            "n": n,
            "entropy": entropy,
            "communication_complexity": communication_complexity
        })
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["entropy"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["communication_complexity"] >= result["entropy"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Communication Complexity vs Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")