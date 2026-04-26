import random
import math
from fractions import Fraction

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
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1)**(i+2)
    det %= mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[matrix_minor(matrix, j, i) * (-1)**(j+i) for i in range(n)] for j in range(n)]
    return [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]

def matrix_minor(matrix, row, col):
    minor = [row[:col] + row[col+1:] for row in matrix[1:]]
    return determinant(minor)

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix)):
        det += ((-1)**i) * matrix[0][i] * determinant([row[:i] + row[i+1:] for row in matrix[1:]])
    return det

def is_semifield_entry(entry):
    if entry == 0:
        return True
    if entry == 1:
        return True
    if entry % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(entry)) + 1, 2):
        if entry % i == 0:
            return False
    return True

def smallest_semifield_order(matrix):
    entries = set()
    for row in matrix:
        for entry in row:
            entries.add(entry)
    q = max(entries) + 1
    while not all(is_semifield_entry(entry) for entry in entries):
        q += 1
    return q

def nisan_wigderson_seed_length(matrix, mod):
    inv_matrix = matrix_mod_inv(matrix, mod)
    seed_length = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != inv_matrix[i][j]:
                seed_length += math.ceil(math.log2(abs(matrix[i][j] - inv_matrix[i][j])))
    return seed_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    mod = smallest_semifield_order(matrix)
    seed_length = nisan_wigderson_seed_length(matrix, mod)
    expected_seed_length = math.log2(mod)
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": abs(seed_length - expected_seed_length) < 0.5 * expected_seed_length,
        "counterexample": "" if conjecture_holds else f"Seed length {seed_length} does not match expected {expected_seed_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_seed_length = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_seed_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_seed_length} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Seed length does not match expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")