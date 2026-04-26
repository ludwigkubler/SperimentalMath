import random
import math
from collections import defaultdict

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

def adjacency_matrix(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for u, v in G:
        A[u][v] = 1
        A[v][u] = 1
    return A

def eigenvalues(A):
    n = len(A)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    lambda_max = max(abs(eigenvalue) for eigenvalue in numpy.linalg.eigvals(A))
    return lambda_max

def tseitin_formula(G, n):
    clauses = []
    for u in range(n):
        literals = [f"x_{u}_{i}" for i in range(n)]
        clauses.append(["~" + literals[0]] + literals[1:])
        for v in range(u + 1, n):
            literals_u = [f"x_{u}_{i}" for i in range(n)]
            literals_v = [f"x_{v}_{i}" for i in range(n)]
            clauses.append([f"~{literals_u[0]}", f"{literals_v[0]}"])
            clauses.append([f"~{literals_v[0]}", f"{literals_u[0]}"])
    return clauses

def resolution_width(clauses):
    queue = [set(clause) for clause in clauses]
    learned_clauses = []
    while queue:
        unit_clause = next((clause for clause in queue if len(clause) == 1), None)
        if not unit_clause:
            break
        literal = list(unit_clause)[0]
        queue.remove(unit_clause)
        learned_clauses.append(unit_clause)
        new_clauses = set()
        for clause in queue:
            if literal in clause:
                new_clauses.add(clause - {literal})
            elif "~" + literal in clause:
                new_clauses.add(clause - {"~" + literal} | {-literal})
        queue.extend(new_clauses)
    return len(learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 15
    d = 4
    G = [(u, (u + v) % n) for u in range(n) for v in range(1, d // 2 + 1)]
    A = adjacency_matrix(G)
    lambda_2 = eigenvalues(A)[1]
    T = tseitin_formula(G, n)
    width = resolution_width(T)
    c = 0.5
    conjecture_holds = width >= c * lambda_2 / math.sqrt(math.log(n))
    counterexample = "" if conjecture_holds else f"Width {width} < {c * lambda_2 / math.sqrt(math.log(n))}"
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
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

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")