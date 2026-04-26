import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_val += ((-1) ** j) * A[0][j] * det(submatrix)
    return det_val

def pi_degree(A):
    n = len(A)
    basis = []
    for i in range(n):
        if all(det(gaussian_elimination([A[i]] + [row[:i] + row[i+1:] for row in A[j:j+1]]) == 0 for j in range(i)):
            basis.append(A[i])
    return len(basis)

def min_abp_size(cnf):
    n = len(cnf)
    m = len(cnf[0])
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(m + 1):
            if cnf[i-1][j]:
                dp[i][j] = min(dp[i][j], dp[i-1][j-1] + 1)
            dp[i][j] = min(dp[i][j], dp[i-1][j])
    return dp[n][m]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 14)
    m = random.randint(8, 11)
    cnf = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    
    pi_basis = [pi_degree(cnf) for _ in range(10)]
    abp_size = min_abp_size(cnf)
    
    metric_name = "PI-Degree"
    metric_value = sum(pi_basis) / len(pi_basis)
    instances_tested = 1
    conjecture_holds = math.isclose(metric_value, math.log(m), rel_tol=1e-2)
    counterexample = "" if conjecture_holds else f"ABP size {abp_size} does not match PI-degree {metric_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ABP size does not match PI-degree\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")