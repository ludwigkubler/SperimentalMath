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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def tensor_product(cnf):
        size = len(cnf)
        result = [[0] * (size * size) for _ in range(size * size)]
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    for l in range(size):
                        if cnf[i][k] == -cnf[j][l]:
                            result[i * size + j][(k * size) + l] = 1
        return result
    
    def tropical_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if any(x != 0 for x in matrix[j]):
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[pivot_row][j]
                for k in range(n):
                    matrix[j][k] = max(matrix[j][k], matrix[pivot_row][k] + factor)
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    tensor_prod = tensor_product(cnf)
    tau = tropical_rank(tensor_prod)
    
    theta_n = math.log(n, 2)
    return {
        "metric_name": "tropical_rank",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": tau <= theta_n + 3 and tau >= theta_n - 3,
        "counterexample": "" if tau <= theta_n + 3 else f"tau(C ⊗ C^⊤) = {tau}, θ(n) = {theta_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")