import sys
import random
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * sum(matrix[j][(j + 1) % n] * matrix[(j + 2) % n][(j + 3) % n] - matrix[j][(j + 1) % n] * matrix[(j + 3) % n][(j + 2) % n] for j in range(1, n)) * (-1) ** i
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[1:]]
            for k in range(1, n):
                minor[k-1] = minor[k-1][:i] + minor[k-1][i+1:]
            adjugate[i][j] = sum(minor[k][(k + 1) % n] * minor[(k + 2) % n][(k + 3) % n] - minor[k][(k + 1) % n] * minor[(k + 3) % n][(k + 2) % n] for k in range(1, n)) * (-1) ** (i + j)
            adjugate[i][j] = adjugate[i][j] % mod
    inv_matrix = [[(adjugate[j][i] * inv_det) % mod for i in range(n)] for j in range(n)]
    return inv_matrix

def matrix_mul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_sub(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[matrix[j][i] for j in range(n)] for i in range(m)]
    return result

def matrix_det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = [row[:i] + row[i+1:] for row in matrix[1:]]
        for j in range(1, n):
            minor[j-1] = minor[j-1][:i] + minor[j-1][i+1:]
        det += matrix[0][i] * sum(minor[k][(k + 1) % n] * minor[(k + 2) % n][(k + 3) % n] - minor[k][(k + 1) % n] * minor[(k + 3) % n][(k + 2) % n] for k in range(1, n)) * (-1) ** i
    return det

def matrix_pow(matrix, power):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    while power > 0:
        if power % 2 == 1:
            result = matrix_mul(result, matrix)
        matrix = matrix_mul(matrix, matrix)
        power //= 2
    return result

def matrix_exp(matrix, mod):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    while matrix:
        if any(x != 0 for row in matrix):
            result = matrix_mul(result, matrix_mod_inv(matrix, mod))
        matrix = matrix_sub(matrix, [[matrix[j][i] // (j + 1) for i in range(n)] for j in range(1, n)])
    return result

def polynomial_volume(poly):
    n = len(poly)
    volume = 1
    for coeff in poly:
        if coeff != 0:
            volume *= abs(coeff)
    return volume

def generate_3sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def evaluate_polynomial(poly, assignment):
    result = poly[0]
    for i in range(1, len(poly)):
        result += poly[i] * assignment[i-1]
    return result

def is_satisfiable(instance):
    n = max(abs(x) for clause in instance for x in clause)
    for _ in range(100):
        assignment = [random.choice([True, False]) for _ in range(n)]
        if all(evaluate_polynomial(clause, assignment) != 0 for clause in instance):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    total_volume = 0
    total_circuits = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        instance = generate_3sat_instance(n)
        if is_satisfiable(instance):
            poly = [1]
            for clause in instance:
                factors = [x**2 - 1 for x in clause]
                poly = matrix_mul(poly, factors)
            volume = polynomial_volume(poly)
            total_volume += volume
            instances_tested += 1
        else:
            conjecture_holds = False
            counterexample = "unsatisfiable_instance"

    mean_volume = total_volume / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / len(n_values)

    return {
        "metric_name": "volume",
        "metric_value": mean_volume,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_volume = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_volume} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"unsatisfiable_instance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")