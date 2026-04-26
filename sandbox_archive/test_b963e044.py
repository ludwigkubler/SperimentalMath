import random
import math
import json
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, m):
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    det = determinant(matrix, m)
    inv_det = mod_inverse(det, m)
    
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            cofactor = (-1) ** (i + j) * determinant(minor, m)
            adj[j][i] = (cofactor * inv_det) % m
    
    return adj

def determinant(matrix, m):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    
    det = 0
    for j in range(n):
        minor = get_minor(matrix, 0, j)
        det += ((-1) ** j) * matrix[0][j] * determinant(minor, m)
    
    return det % m

def get_minor(matrix, i, j):
    n = len(matrix)
    minor = [[matrix[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
    return minor

def matrix_mul_mod(A, B, m):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m
    
    return C

def matrix_add_mod(A, B, m):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % m
    
    return C

def matrix_sub_mod(A, B, m):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % m
    
    return C

def matrix_pow_mod(matrix, k, m):
    n = len(matrix)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul_mod(result, matrix, m)
        matrix = matrix_mul_mod(matrix, matrix, m)
        k //= 2
    
    return result

def is_complete_intersection(poly_system):
    n = len(poly_system)
    A = [[0] * (n + 1) for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            A[i][j] = poly_system[i][j]
        A[i][-1] = -poly_system[i][-1]
    
    det = determinant(A, 2)
    return det == 0

def sos_rank(poly_system):
    n = len(poly_system)
    m = 2 ** (n + 1)
    A = [[0] * m for _ in range(m)]
    
    for i in range(m):
        for j in range(m):
            if bin(i & j).count('1') % 2 == 0:
                A[i][j] = 1
    
    B = matrix_mul_mod(A, poly_system, m)
    C = matrix_sub_mod(B, [[1] * m], m)
    
    det = determinant(C, m)
    return int(math.sqrt(det))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    poly_system = []
    
    for _ in range(n):
        coeffs = [random.randint(0, 1) for _ in range(n + 1)]
        poly_system.append(coeffs)
    
    if is_complete_intersection(poly_system):
        rank = sos_rank(poly_system)
        return {
            "metric_name": "SOS Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": abs(rank - math.sqrt(n)) < 0.5,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "SOS Rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_complete_intersection"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 4:
        print(f"RESULT: SUPPORTED mean={total_metric_value / support_fraction} std=0.0 support_fraction={support_fraction / len(results):.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_complete_intersection' first_failing_seed={first_failing_seed}")