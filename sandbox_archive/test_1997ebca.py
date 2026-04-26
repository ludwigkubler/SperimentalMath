import random
import math
import sys
from typing import Dict, List, Tuple

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    
    def gaussian_elimination(A: List[List[float]]) -> List[List[float]]:
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def cross_correlation_flow_norm(C: List[List[float]]) -> float:
        n = len(C)
        norm = 0
        for i in range(n):
            for j in range(i + 1, n):
                norm += abs(C[i][j])
        return norm

    def kolmogorov_sinai_entropy(C: List[List[float]], T: List[List[int]]) -> float:
        n = len(C)
        entropy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if T[i][j] != T[j][i]:
                    entropy += math.log2(abs(C[i][j]))
        return entropy

    def communication_complexity(C: List[List[float]], T: List[List[int]]) -> float:
        n = len(C)
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if T[i][j] != T[j][i]:
                    complexity += abs(C[i][j])
        return complexity

    def generate_circuit(n: int) -> Tuple[List[List[float]], List[List[int]]]:
        A = [[random.random() for _ in range(n)] for _ in range(n)]
        B = gaussian_elimination(A)
        C = matrix_multiply(B, A)
        T = [[0 if i == j else 1 if random.randint(0, 1) else -1 for j in range(n)] for i in range(n)]
        return C, T

    def estimate_entropy(C: List[List[float]], n: int) -> float:
        entropy = 0
        for _ in range(100):
            C_est = generate_circuit(n)[0]
            entropy += kolmogorov_sinai_entropy(C_est, C)
        return entropy / 100

    def estimate_complexity(C: List[List[float]], n: int) -> float:
        complexity = 0
        for _ in range(100):
            C_est = generate_circuit(n)[0]
            complexity += communication_complexity(C_est, C)
        return complexity / 100

    def cross_correlation_flow_norm(C: List[List[float]]) -> float:
        n = len(C)
        norm = 0
        for i in range(n):
            for j in range(i + 1, n):
                norm += abs(C[i][j])
        return norm

    n_values = [5, 8, 11, 14]
    results = []
    for n in n_values:
        C, T = generate_circuit(n)
        entropy = estimate_entropy(C, n)
        cross_corr_norm = cross_correlation_flow_norm(C)
        complexity = estimate_complexity(C, n)
        results.append({
            "n": n,
            "entropy": entropy,
            "cross_corr_norm": cross_corr_norm,
            "complexity": complexity
        })

    mean_entropy = sum(r["entropy"] for r in results) / len(results)
    mean_cross_corr_norm = sum(r["cross_corr_norm"] for r in results) / len(results)
    mean_complexity = sum(r["complexity"] for r in results) / len(results)

    conjecture_holds = all(mean_entropy > math.log2(n) and mean_cross_corr_norm > 0.1 * n**0.5 for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")