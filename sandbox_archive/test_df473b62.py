import sys
import random
import math
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

def matrix_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_pow(M, p):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, M)
        M = matrix_mul(M, M)
        p //= 2
    return result

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_semidfields(q):
    if q < 4:
        return []
    if q & (q - 1) != 0:
        return []
    p = q.bit_length() - 1
    if not is_prime(p):
        return []
    n = q - 1
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    if len(factors) != 2 or factors[0] * factors[1] != q - 1:
        return []
    a, b = factors
    subfields = []
    for k in range(1, min(a, b) + 1):
        if gcd(k, a) == gcd(k, b) == 1:
            subfields.append(q // (k * k))
    return sorted(subfields)

def generate_primitive_element(q):
    if q < 4:
        return None
    p = q.bit_length() - 1
    if not is_prime(p):
        return None
    n = q - 1
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    if len(factors) != 2 or factors[0] * factors[1] != q - 1:
        return None
    a, b = factors
    for g in range(2, q):
        if pow(g, a, q) == 1 and pow(g, b, q) == 1:
            return g
    return None

def characteristic_function(subgroup):
    n = len(subgroup)
    result = [0] * (n + 1)
    for i in range(n):
        result[subgroup[i]] = 1
    return result

def simulate_acc0_circuit(characteristic, depth):
    n = len(characteristic)
    dp = [[float('inf')] * (1 << n) for _ in range(depth + 1)]
    dp[0][0] = 0
    for d in range(1, depth + 1):
        for state in range(1 << n):
            for i in range(n):
                if (state >> i) & 1:
                    new_state = state ^ (1 << i)
                    cost = dp[d - 1][new_state] + characteristic[i]
                    dp[d][state] = min(dp[d][state], cost)
    return dp[depth][(1 << n) - 1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [4, 8, 16]
    results = []
    for q in q_values:
        subfields = generate_semidfields(q)
        if not subfields:
            return {
                "metric_name": "subfield_count",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        primitive_element = generate_primitive_element(q)
        if not primitive_element:
            return {
                "metric_name": "subfield_count",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        subgroup = [pow(primitive_element, i, q) for i in range(q - 1)]
        characteristic = characteristic_function(subgroup)
        circuit_size = simulate_acc0_circuit(characteristic, q.bit_length() - 1)
        results.append({
            "q": q,
            "subfield_count": len(subfields),
            "circuit_size": circuit_size
        })
    subfield_counts = [r["subfield_count"] for r in results]
    circuit_sizes = [r["circuit_size"] for r in results]
    if all(sc == cs for sc, cs in zip(subfield_counts, circuit_sizes)):
        return {
            "metric_name": "subfield_count",
            "metric_value": subfield_counts[0],
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for i in range(len(subfield_counts)):
            if subfield_counts[i] != circuit_sizes[i]:
                return {
                    "metric_name": "subfield_count",
                    "metric_value": None,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"q={results[i]['q']}: subfield_count={subfield_counts[i]}, circuit_size={circuit_sizes[i]}"
                }
        return {
            "metric_name": "subfield_count",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    subfield_counts = [r["metric_value"] for r in results if r["conjecture_holds"]]
    circuit_sizes = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(subfield_counts) / len(results)
    mean_subfield_count = sum(subfield_counts) / len(subfield_counts) if subfield_counts else None
    std_subfield_count = math.sqrt(sum((x - mean_subfield_count) ** 2 for x in subfield_counts) / len(subfield_counts)) if subfield_counts else None

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_subfield_count} std={std_subfield_count} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")