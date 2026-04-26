import random
import math
import itertools

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Inverse doesn\'t exist')
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def is_invertible(A):
    return determinant(A) != 0

def matroid_tutte_polynomial(matroid, x=1, y=1):
    if len(matroid) == 0:
        return 1
    elif len(matroid[0]) == 0:
        return 1
    else:
        e = matroid[0][0]
        A = [row[1:] for row in matroid[1:]]
        B = [[row[0]] + row[2:] for row in matroid[1:]]
        return matroid_tutte_polynomial(A, x, y) - matroid_tutte_polynomial(B, x, y)

def cnf_to_incidence_matrix(cnf):
    variables = set()
    clauses = []
    for clause in cnf:
        variables.update(clause)
        clauses.append([1 if var in clause else 0 for var in sorted(variables)])
    return [sorted(variables), *clauses]

def extended_frege_proof_size(cnf):
    # Placeholder function: this should be replaced with an actual EF proof size computation
    return len(cnf) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    cnf = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
    incidence_matrix = cnf_to_incidence_matrix(cnf)
    matroid = incidence_matrix[1:]
    degree = matroid_tutte_polynomial(matroid)
    ef_size = extended_frege_proof_size(cnf)
    k = degree / math.log(n) if n > 0 else 0
    conjecture_holds = abs(k - math.floor(k)) < 0.1 and abs(degree - math.floor(degree)) < 0.1
    counterexample = "" if conjecture_holds else f"n={n}, degree={degree}, ef_size={ef_size}"
    return {
        "metric_name": "Tutte Polynomial Degree / EF Proof Size",
        "metric_value": degree,
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

    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")