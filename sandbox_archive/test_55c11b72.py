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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses

    def karchmer_wigderson_protocol(n):
        cnf = generate_3cnf(n)
        protocol = []
        for clause in cnf:
            protocol.extend([abs(x) for x in clause if x > 0])
        return protocol

    def voiculescu_transform(matrix):
        n = len(matrix)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = matrix[i][j] / (1 + sum(matrix[k][l] for k in range(n) if k != i and l != j))
        return result

    def r_transform(matrix):
        n = len(matrix)
        result = [0] * n
        for i in range(n):
            for j in range(n):
                result[i] += matrix[i][j]
        return result

    def norm(vector):
        return sum(x**2 for x in vector) ** 0.5

    n = 40
    protocol = karchmer_wigderson_protocol(n)
    transition_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                transition_matrix[i][j] = 1 / (i + j - 1)
    
    voiculescu_mat = voiculescu_transform(transition_matrix)
    r_values = r_transform(voiculescu_mat)
    rho = abs(r_values[0])
    
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 3.5,
        "counterexample": "" if rho >= 3.5 else "rho < 3.5"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={math.sqrt(sum((r['metric_value'] - mean_rho)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 3.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")