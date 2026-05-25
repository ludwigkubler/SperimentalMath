# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
            cnf.append(clause)
    return cnf

def tensor_product(cnf):
    n = len(cnf)
    m = len(cnf[0])
    result = [[0] * (m * m) for _ in range(n * n)]
    for i in range(n):
        for j in range(m):
            for k in range(n):
                for l in range(m):
                    if cnf[i][j] == -cnf[k][l]:
                        result[i * m + j][(k * m) + l] = 1
                    elif cnf[i][j] == cnf[k][l]:
                        result[i * m + j][(k * m) + l] = -1
    return result

def tropical_rank(matrix):
    n = len(matrix)
    for i in range(n):
        matrix[i][i] += 1
    for k in range(n):
        for i in range(n):
            if i != k:
                factor = matrix[i][k]
                for j in range(n):
                    matrix[i][j] = max(matrix[i][j], factor + matrix[k][j])
    return max(sum(row) for row in matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = random_cnf(n, n * (n - 1))
        tensor_prod = tensor_product(cnf)
        rank = tropical_rank(tensor_prod)
        theta_n = math.log(n)
        
        if rank > theta_n + 3 or rank < theta_n - 3:
            return {
                "metric_name": "tropical_rank",
                "metric_value": rank,
                "instances_tested": len(cnf),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, θ(n)={theta_n}"
            }
        
        results.append(rank)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if theta_n - 3 <= r <= theta_n + 3]) / len(results)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean,
        "instances_tested": sum(len(cnf) for n, cnf in zip(n_values, [random_cnf(n, n * (n - 1)) for n in n_values])),
        "conjecture_holds": support_fraction >= 0.8333,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8333:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")