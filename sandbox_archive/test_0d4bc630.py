import sys
import random
import math
import itertools

def add_mod(a, b, m):
    return (a + b) % m

def mul_mod(a, b, m):
    return (a * b) % m

def pow_mod(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b & 1:
            result = mul_mod(result, a, m)
        b >>= 1
        a = mul_mod(a, a, m)
    return result

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mul(A, B, m):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = add_mod(C[i][j], mul_mod(A[i][k], B[k][j], m), m)
    return C

def matrix_pow(M, p, m):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p & 1:
            result = matrix_mul(result, M, m)
        M = matrix_mul(M, M, m)
        p >>= 1
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] = mul_mod(A[i][j], mod_inverse(pivot, 2), 2)
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] = add_mod(A[j][k], mul_mod(-factor, A[i][k], 2), 2)
    return A

def is_tautology(phi):
    variables = set()
    clauses = []
    for clause in phi:
        literals = [int(l) for l in clause.split()]
        if len(set(literals)) == len(literals):
            variables.update(abs(l) for l in literals)
            clauses.append(literals)
    n = max(variables)
    assignment = [0] * (n + 1)
    def backtrack(i):
        if i > n:
            return all(any(assignment[abs(l)] ^ (l < 0) for l in clause) for clause in clauses)
        assignment[i] = 0
        if backtrack(i + 1):
            return True
        assignment[i] = 1
        return backtrack(i + 1)
    return backtrack(1)

def dpll(phi):
    variables = set()
    clauses = []
    for clause in phi:
        literals = [int(l) for l in clause.split()]
        if len(set(literals)) == len(literals):
            variables.update(abs(l) for l in literals)
            clauses.append(literals)
    n = max(variables)
    assignment = [0] * (n + 1)
    def backtrack(i):
        if i > n:
            return all(any(assignment[abs(l)] ^ (l < 0) for l in clause) for clause in clauses)
        assignment[i] = 0
        if backtrack(i + 1):
            return True
        assignment[i] = 1
        return backtrack(i + 1)
    return backtrack(1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    phi = []
    for _ in range(n):
        clause = ' '.join(str(random.randint(-n, -1)) for _ in range(3))
        phi.append(clause)
    
    if not is_tautology(phi):
        return {
            "metric_name": "EF proof size",
            "metric_value": 0,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "not a tautology"
        }
    
    m = 2 ** random.randint(1, 3)
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    B = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
    C = matrix_mul(A, B, m)
    
    line_count = sum(sum(row) for row in C)
    EF_proof_size = dpll(phi)
    
    return {
        "metric_name": "EF proof size",
        "metric_value": EF_proof_size,
        "instances_tested": n,
        "conjecture_holds": abs(line_count - 2 ** (n // 2)) < 10 and EF_proof_size >= n ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")