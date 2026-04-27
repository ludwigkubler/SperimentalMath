# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def generate_3cnf(n, density):
    clauses = []
    for _ in range(int(density * n * (n - 1) / 2)):
        clause = [random.randint(-n, n) for _ in range(3)]
        while len(set(clause)) != 3:
            clause = [random.randint(-n, n) for _ in range(3)]
        clauses.append(tuple(sorted(clause)))
    return clauses

def is_satisfiable(clauses):
    n = max(abs(c) for clause in clauses)
    assignments = list(itertools.product([0, 1], repeat=n))
    for assignment in assignments:
        if all(any(x == y or x == -y for x, y in zip(assignment, clause)) for clause in clauses):
            return True
    return False

def walsh_hadamard_transform(vector):
    n = len(vector)
    if n == 1:
        return vector
    even = walsh_hadamard_transform(vector[::2])
    odd = walsh_hadamard_transform(vector[1::2])
    result = [0] * n
    for i in range(n // 2):
        result[i] = even[i] + odd[i]
        result[i + n // 2] = even[i] - odd[i]
    return result

def hypercontractive_defect(A_F, p_values):
    H_F = []
    for p in p_values:
        T_p = [0] * len(A_F)
        for i in range(len(A_F)):
            T_p[i] = sum(A_F[j] * A_F[k] for j in range(i + 1) for k in range(j, len(A_F)) if (j - k) % p == 0 and j != k)
        norm_2 = math.sqrt(sum(x**2 for x in T_p))
        norm_p = sum(abs(x)**p for x in A_F) ** (1 / p)
        H_F.append(math.log(norm_2 / norm_p))
    return max(H_F)

def resolution_width(clauses):
    n = max(abs(c) for clause in clauses)
    queue = list(range(n + 1))
    while queue:
        width = queue.pop(0)
        new_queue = []
        for i in range(width, n + 1):
            if any(all(x == y or x == -y for x, y in zip(clauses[j], clause)) for j in range(len(queue))):
                new_queue.append(i + 1)
        if not new_queue:
            return width
        queue.extend(new_queue)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p_values = [1.1, 1.3, 1.5, 1.7, 1.9]
    support_count = 0
    equality_count = 0
    counterexample = ""
    
    for n in {8, 10, 12, 14}:
        for density in {4.4, 4.6, 4.8, 5.0}:
            for _ in range(10):
                clauses = generate_3cnf(n, density)
                if is_satisfiable(clauses):
                    continue
                A_F = [1 if any(x == y or x == -y for x, y in zip(clause, assignment)) else 0 for clause in clauses for assignment in itertools.product([0, 1], repeat=n)]
                H_F = hypercontractive_defect(A_F, p_values)
                w_F = resolution_width(clauses)
                if w_F >= math.ceil(H_F / math.log2(n + 1)):
                    support_count += 1
                    if density == 4.6:
                        equality_count += 1
    
    conjecture_holds = support_count == 40 * 4 * 10
    equality_fraction = equality_count / (40 * 4 * 10)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_F,
        "instances_tested": 40 * 4 * 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")