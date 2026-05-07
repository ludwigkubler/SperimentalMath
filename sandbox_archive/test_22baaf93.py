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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = rank
        for i in range(rank, rows):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if matrix[i_max][j] == 0:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rows):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = random.randint(n // 2, n * (n - 1) // 2)
    variables = list(range(n))
    clauses = []
    for _ in range(num_clauses):
        clause = random.sample(variables, 3)
        clauses.append(clause)

    incidence_matrix = [[0] * n for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            incidence_matrix[i][var] = 1

    rank = gaussian_elimination(incidence_matrix)
    
    # Known ACC^0 circuit sizes for benchmark formulas
    if n == 2:
        known_circuit_size = 1
    elif n == 3:
        known_circuit_size = 4
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    # Check if the rank satisfies the conjecture
    if rank >= math.log(n, 2):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Rank {rank} does not satisfy log n for n={n}"

    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = [r["seed"] for r in results if not r["conjecture_holds"]][0]
        print(f"RESULT: FALSIFIED counterexample=\"rank does not satisfy log n\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")