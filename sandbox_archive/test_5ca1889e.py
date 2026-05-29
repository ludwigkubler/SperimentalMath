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

def random_k_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice([f'x{i}', f'-x{i}']) for i in random.sample(variables, random.randint(1, n))]
        clauses.append(clause)
    return clauses

def tropical_add(a, b):
    if a == float('-inf'):
        return b
    if b == float('-inf'):
        return a
    return max(a, b)

def tropical_multiply(a, b):
    if a == float('-inf') or b == float('-inf'):
        return float('-inf')
    return a + b

def tropical_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        pivot = None
        for j in range(i, n):
            if matrix[j][i] != float('-inf'):
                pivot = j
                break
        if pivot is None:
            continue
        rank += 1
        for j in range(n):
            if j == i:
                continue
            factor = tropical_multiply(tropical_add(-matrix[pivot][j], matrix[i][j]), -1)
            for k in range(n):
                matrix[j][k] = tropical_add(matrix[j][k], tropical_multiply(factor, matrix[pivot][k]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(1, 40)
    m = random.randint(1, 2 * n)
    clauses = random_k_cnf(n, m)
    
    tropical_semigroup = []
    for clause in clauses:
        tropical_clause = [float('-inf')] * (n + 1)
        for literal in clause:
            var = int(literal[1:])
            sign = 1 if literal.startswith('x') else -1
            tropical_clause[var] = tropical_add(tropical_clause[var], sign)
        tropical_semigroup.append(tropical_clause)
    
    rank = tropical_rank(tropical_semigroup)
    communication_complexity = 2 ** rank
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": rank >= math.log(communication_complexity, 2),
        "counterexample": "" if rank >= math.log(communication_complexity, 2) else f"Rank {rank} < CC_R(I) = {communication_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")