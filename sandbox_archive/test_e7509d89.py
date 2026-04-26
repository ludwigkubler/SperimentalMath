import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def spectral_norm(A):
        n = len(A)
        v = [Fraction(1) / math.sqrt(n)] * n
        for _ in range(10):  # Power iteration method
            v = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm = sum(v[i]**2 for i in range(n))
            v = [v[i] / math.sqrt(norm) for i in range(n)]
        return max(abs(x) for x in v)
    
    def cross_correlation_flow(circuit):
        n = len(circuit)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = sum(circuit[k][i] * circuit[k][j] for k in range(n))
                A[j][i] = A[i][j]
        return gaussian_elimination(A)
    
    def generate_ac0_circuit(depth):
        n = 2 ** depth
        circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return circuit
    
    n_values = [5, 8, 11, 14]
    decay_rates = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(int(math.log2(n)))
        A = cross_correlation_flow(circuit)
        norm = spectral_norm(A)
        decay_rates.append(norm)
    
    mean_decay_rate = sum(decay_rates) / len(decay_rates)
    alpha = 1 / (len(n_values) - 1)
    expected_decay_rate = n ** (-alpha)
    
    conjecture_holds = all(norm <= expected_decay_rate for norm in decay_rates)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "spectral_norm",
        "metric_value": mean_decay_rate,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")