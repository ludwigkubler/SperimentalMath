import random
import math
import itertools
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i, n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += A[i][j] ** 2
        return math.sqrt(norm)
    
    def symbolic_dynamics(C, T, n):
        k = len(C)
        states = list(itertools.product(range(k), repeat=n))
        transitions = defaultdict(int)
        for state in states:
            next_state = tuple((T[state[i]][state[(i + 1) % n]] for i in range(n)))
            transitions[(state, next_state)] += 1
        return transitions
    
    def kolmogorov_entropy(transitions):
        total_transitions = sum(transitions.values())
        entropy = 0
        for count in transitions.values():
            prob = count / total_transitions
            entropy -= prob * math.log2(prob)
        return entropy
    
    n = random.choice([5, 8, 11, 14])
    k = 3
    C = [[random.randint(0, 1) for _ in range(k)] for _ in range(k)]
    T = [[[random.randint(0, 1) for _ in range(k)] for _ in range(n)] for _ in range(k)]
    
    F = gaussian_elimination(C)
    norm_F = frobenius_norm(F)
    
    transitions = symbolic_dynamics(C, T, n)
    K = kolmogorov_entropy(transitions)
    
    return {
        "metric_name": "Kolmogorov Entropy",
        "metric_value": K,
        "instances_tested": 1,
        "conjecture_holds": norm_F <= 0.5 and K < n / math.log(n),
        "counterexample": "" if norm_F <= 0.5 and K < n / math.log(n) else f"Counterexample with F norm {norm_F} and K={K}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius norm too high or entropy too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")