import random
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
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
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det
    
    def extended_frege_size(n):
        # Placeholder function to simulate EF proof size
        return 2 ** n
    
    def column_matroid_tutte_polynomial_degree(A):
        m, n = len(A), len(A[0])
        if m == 1:
            return 1
        if n == 1:
            return determinant(A)
        
        A1 = [row[:n-1] for row in A]
        A2 = [row[n:] for row in A]
        det_A1 = determinant(A1)
        det_A2 = determinant(A2)
        
        degree = column_matroid_tutte_polynomial_degree(A1) + column_matroid_tutte_polynomial_degree(A2)
        return degree
    
    n = random.randint(5, 14)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    degree = column_matroid_tutte_polynomial_degree(A)
    ef_size = extended_frege_size(n)
    
    k = degree / math.log(n) if n > 0 else 0
    
    return {
        "metric_name": "Tutte Polynomial Degree",
        "metric_value": k,
        "instances_tested": 1,
        "conjecture_holds": abs(k - math.log(n)) < 0.5 * math.log(n),
        "counterexample": "" if abs(k - math.log(n)) < 0.5 * math.log(n) else f"n={n}, degree={degree}, log(n)={math.log(n)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_degree = 0
    count_supporting = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
        total_degree += result["metric_value"]
        if result["conjecture_holds"]:
            count_supporting += 1
    
    mean_degree = total_degree / len(results)
    support_fraction = count_supporting / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_degree} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")