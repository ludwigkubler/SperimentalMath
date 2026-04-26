import random
import math
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        augmented_matrix = [A[i] + [0] * (n - m) for i in range(m)] + [[1 if j == i else 0 for j in range(n)] for i in range(n - m)]
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            factor = augmented_matrix[i][i]
            for j in range(i, n):
                augmented_matrix[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[n:] for row in augmented_matrix[:m]]
    
    def frobenius_norm(A):
        norm = 0
        for row in A:
            for val in row:
                norm += abs(val) ** 2
        return math.sqrt(norm)
    
    def compute_kolmogorov_entropy(C, T, n):
        # Simplified symbolic dynamics approach for small n
        partition = [[i] for i in range(n)]
        entropy = 0
        for _ in range(10):  # Simulate 10 time steps
            new_partition = []
            for block in partition:
                new_block = set()
                for x in block:
                    new_block.update(T[x])
                new_partition.append(list(new_block))
            entropy += math.log(len(new_partition) / len(partition))
            partition = new_partition
        return entropy
    
    def compute_cross_correlation_flow(C, T, n):
        # Simplified numerical integration approach for small n
        flow = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    flow[i][j] = sum(1 for x in range(n) if T[x][i] == T[x][j])
        return flow
    
    def is_sublinear_growth(K, n):
        # Fit a regression model to check sublinear growth
        coefficients = [K[i] / (i + 1) for i in range(len(K))]
        avg_coefficient = sum(coefficients) / len(coefficients)
        return all(coef <= avg_coefficient for coef in coefficients)
    
    n = random.choice([5, 8, 11, 14])
    C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    T = {i: set(random.sample(range(n), random.randint(1, n // 2))) for i in range(n)}
    
    F = compute_cross_correlation_flow(C, T, n)
    K = compute_kolmogorov_entropy(C, T, n)
    
    frobenius_norm_F = frobenius_norm(F)
    conjecture_holds = is_sublinear_growth([K], n) if frobenius_norm_F < 1 else False
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Frobenius norm",
        "metric_value": frobenius_norm_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
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
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")