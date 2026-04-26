import random
import math
import sys
import json

def max_plus_add(a, b):
    return max(a, b)

def max_plus_mul(a, b):
    if a == -math.inf or b == -math.inf:
        return -math.inf
    return a + b

def tropical_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        pivot_row = None
        for j in range(i, n):
            if matrix[j][i] != -math.inf:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        rank += 1
        for j in range(n):
            if j == i:
                continue
            factor = max_plus_mul(-matrix[pivot_row][j], matrix[i][i])
            for k in range(n):
                matrix[j][k] = max_plus_add(matrix[j][k], max_plus_mul(factor, matrix[pivot_row][k]))
    return rank

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) if random.choice([True, False]) else -v for v in variables]
        clauses.append(clause)
    return clauses

def cnf_to_tropical_matrix(cnf):
    n = len(cnf[0])
    matrix = [[-math.inf] * n for _ in range(n)]
    for clause in cnf:
        for i, x in enumerate(clause):
            if x > 0:
                matrix[x - 1][i] = 0
    return matrix

def acc_circuit_size(cnf):
    n = len(cnf[0])
    m = len(cnf)
    size = 0
    for clause in cnf:
        size += 1 + len(clause) - 1
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    matrix = cnf_to_tropical_matrix(cnf)
    rank = tropical_rank(matrix)
    circuit_size = acc_circuit_size(cnf)
    conjecture_holds = (rank == math.log2(n) and circuit_size <= n**2) or (rank != math.log2(n) and circuit_size > n**2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {json.dumps(result)}")
    
    total_rank = sum(r["metric_value"] for r in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")