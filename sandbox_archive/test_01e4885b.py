import random
import math
import sys
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def monte_carlo_orbit_signature(C, T, n_samples=10000):
        m = len(C)
        orbit_signature = [0] * m
        for _ in range(n_samples):
            x = random.randint(0, 2**m - 1)
            for _ in range(m):
                x = T[x]
            orbit_signature[bin(x).count('1')] += 1
        return [v / n_samples for v in orbit_signature]
    
    def kolmogorov_flow(C, T, max_iter=1000):
        m = len(C)
        flow = [[0] * m for _ in range(m)]
        for i in range(m):
            x = random.randint(0, 2**m - 1)
            for j in range(max_iter):
                x = T[x]
                flow[i][x] += 1
        return flow
    
    def l2_norm(v):
        return math.sqrt(sum(x**2 for x in v))
    
    def sub_exponential_decay(decay_rate, n):
        return decay_rate < (n ** (-0.5 + 1e-6))
    
    def sublinear_growth(growth_rate, n):
        return growth_rate < n
    
    n = random.choice([5, 8, 11, 14])
    m = 2**n
    C = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
    T = [random.randint(0, m-1) for _ in range(m)]
    
    orbit_signature = monte_carlo_orbit_signature(C, T)
    decay_rate = l2_norm([orbit_signature[i] / (i+1) for i in range(len(orbit_signature))])
    flow = kolmogorov_flow(C, T)
    growth_rate = sum(sum(flow[i][j] for j in range(m)) for i in range(m))
    
    conjecture_holds = sub_exponential_decay(decay_rate, n) and not sublinear_growth(growth_rate, n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "decay_rate",
        "metric_value": decay_rate,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    decay_rates = [r["metric_value"] for r in results if "decay_rate" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(decay_rates)/len(decay_rates)} std={math.sqrt(sum((x - sum(decay_rates)/len(decay_rates))**2 for x in decay_rates) / len(decay_rates))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")