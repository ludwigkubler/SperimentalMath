import random
import math
import json
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * sum(matrix[j][(j + i) % n] * (-1) ** (i + j) for j in range(1, n)) % mod
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[sum((-1) ** (i + j) * sum(matrix[k][(k + l) % n] for k in range(i + 1, n)) * matrix[j][(j + l) % n] for l in range(n)) for j in range(n)] for i in range(n)]
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mul(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return result

def matrix_pow(matrix, power):
    if power == 1:
        return matrix
    elif power % 2 == 0:
        half_power = matrix_pow(matrix, power // 2)
        return matrix_mul(half_power, half_power)
    else:
        return matrix_mul(matrix, matrix_pow(matrix, power - 1))

def krull_dimension(ideal):
    n = len(ideal)
    ring_size = 2 ** (n * n)
    basis = [list(range(n)) for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if ideal[i][j] != 0:
                basis[j] = [(i if k == j else k) for k in range(n)]
                break
    return len(basis)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    for n in n_values:
        clauses = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(n)]
        ideal = [[sum(clause[i] * clause[j] for clause in clauses) % 2 for j in range(n)] for i in range(n)]
        dimension = krull_dimension(ideal)
        results.append({
            "n": n,
            "dimension": dimension
        })
    metric_value = sum(result["dimension"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["dimension"] == math.log2(n_values[0] * n_values[1] * n_values[2] * n_values[3]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Krull Dimension",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **trial_result}}))
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")