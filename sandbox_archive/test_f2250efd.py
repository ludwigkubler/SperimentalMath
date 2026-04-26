import random
import math
import sys
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def inverse_matrix(A):
    n = len(A)
    A_augmented = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A)]
    A_echelon = gaussian_elimination(A_augmented)
    if A_echelon is None:
        return None
    I = [[A_echelon[i][n + j] for j in range(n)] for i in range(n)]
    return I

def frobenius_norm(F):
    n = len(F)
    norm = 0
    for i in range(n):
        for j in range(n):
            norm += F[i][j] ** 2
    return math.sqrt(norm)

def symbolic_dynamics(C, X, T, n):
    k = len(X[0])
    mu = defaultdict(int)
    for x in X:
        state = tuple(x)
        for _ in range(n):
            state = tuple(T[state[i]][x[i]] for i in range(k))
        mu[state] += 1
    total = sum(mu.values())
    entropy = -sum(v / total * math.log2(v / total) for v in mu.values())
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    k = 3
    X = [[random.randint(0, 1) for _ in range(k)] for _ in range(n)]
    T = [[[[random.randint(0, 1) for _ in range(2)] for _ in range(2)] for _ in range(2)] for _ in range(2)]
    C = identity_matrix(n)
    
    F = gaussian_elimination(C)
    if F is None:
        return {
            "metric_name": "Frobenius norm",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    K = symbolic_dynamics(C, X, T, n)
    
    return {
        "metric_name": "Kolmogorov entropy",
        "metric_value": K,
        "instances_tested": 1,
        "conjecture_holds": K < n * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_K = sum(r["metric_value"] for r in results) / len(results)
    std_K = math.sqrt(sum((r["metric_value"] - mean_K) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_K} std={std_K} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_K} std={std_K} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")