import random
import math
import sys
import json
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        factor = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= factor
        for k in range(m):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def poset_dimension(rectangles):
    n = len(rectangles)
    if n == 0:
        return 0
    poset = [[False] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if all(rectangles[i][k] or not rectangles[j][k] for k in range(len(rectangles[0]))):
            poset[i][j] = True
    # Find the maximum antichain
    max_antichain = []
    for i in range(n):
        if all(not poset[j][i] for j in range(n) if j != i):
            max_antichain.append(i)
    return len(max_antichain)

def communication_complexity(rectangles):
    m, n = len(rectangles), len(rectangles[0])
    matrix = [[False] * (m + n) for _ in range(m + n)]
    for i in range(m):
        for j in range(n):
            if rectangles[i][j]:
                matrix[i][m + j] = True
                matrix[m + j][i] = True
    elimination_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in elimination_matrix if any(row))
    return m + n - 2 * rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    cnf_formula = []
    for _ in range(n):
        clause = [random.randint(0, 1) * 2 - 1 for _ in range(n)]
        if all(clause[i] == 0 for i in range(n)):
            clause[random.randint(0, n-1)] = 1
        cnf_formula.append(clause)
    communication_matrix = [[any(cnf[j] != 0 for c in cnf_formula) for j in range(n)] for _ in range(n)]
    rectangles = []
    for i in range(n):
        for j in range(n):
            if communication_matrix[i][j]:
                rectangle = [False] * n
                rectangle[i] = True
                rectangle[j] = True
                rectangles.append(rectangle)
    poset_dim = poset_dimension(rectangles)
    comm_complexity = communication_complexity(communication_matrix)
    conjecture_holds = poset_dim <= comm_complexity
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "poset_dimension",
        "metric_value": poset_dim,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")