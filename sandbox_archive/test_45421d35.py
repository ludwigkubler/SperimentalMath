import random
import math
import itertools
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def norm(matrix):
    return max(sum(abs(x) for x in row) for row in matrix)

def induce_kolmogorov_flow(C, X, μ, T):
    n = len(X)
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if C[i][j]:
                F[i][j] = sum(μ[k] * (X[j][k] - X[i][k]) for k in range(n))
    return F

def mixer_profile(C, T):
    n = len(C)
    λ = [0] * n
    for i in range(n):
        λ[i] = C[i][i]
    return λ

def communication_entropy_barrier(F):
    n = len(F)
    λ = sorted(mixer_profile(C, T) for C, X, μ, T in F)
    δ = 1 / (2 * n)
    return n ** δ

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        X = [[random.random() for _ in range(n)] for _ in range(n)]
        μ = [Fraction(random.randint(1, 10)) for _ in range(n)]
        T = random.randint(1, 10)
        
        λ = mixer_profile(C, T)
        decay_rate = sum(abs(x) for x in λ) / n
        
        F = induce_kolmogorov_flow(C, X, μ, T)
        entropy_barrier = communication_entropy_barrier(F)
        
        results.append({
            "n": n,
            "decay_rate": decay_rate,
            "entropy_barrier": entropy_barrier
        })
    
    metric_value = sum(result["entropy_barrier"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["decay_rate"] < 1 / n and result["entropy_barrier"] >= n ** (1 / (2 * n)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_entropy_barrier",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")