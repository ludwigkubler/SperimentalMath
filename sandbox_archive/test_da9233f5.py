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
        for _ in range(2**n // 3):  # Generate a few clauses to make the formula non-trivial
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tropical_hodge_rank(cnf):
        n = len(cnf[0])
        incidence_matrix = [[0] * (2**n) for _ in range(2**n)]
        for i, clause in enumerate(cnf):
            for x in range(2**n):
                if all(x & (1 << abs(lit) - 1) == lit for lit in clause):
                    incidence_matrix[i][x] = 1
        rank = gaussian_elimination(incidence_matrix)
        return rank
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        lead = 0
        for r in range(rows):
            if lead >= cols:
                break
            i = r
            while matrix[i][lead] == 0:
                i += 1
                if i == rows:
                    i = r
                    lead += 1
                    if lead == cols:
                        return r
            matrix[r], matrix[i] = matrix[i], matrix[r]
            for i in range(rows):
                if i != r:
                    factor = matrix[i][lead] / matrix[r][lead]
                    for j in range(lead, cols):
                        matrix[i][j] -= factor * matrix[r][j]
                    matrix[i][lead] = 0
            lead += 1
        return r + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = tropical_hodge_rank(cnf)
        results.append({
            "n": n,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    conjecture_holds = all(0.9 * n**2 / math.log(n) <= rank <= 1.1 * n**2 / math.log(n) for result in results)
    
    return {
        "metric_name": "tropical_hodge_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")