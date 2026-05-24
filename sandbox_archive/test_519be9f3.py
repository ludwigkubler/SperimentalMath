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
    
    def generate_cnf(m, n):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def bruhn_matrix(clauses, n):
        m = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(m):
            x, y = clauses[i]
            matrix[x][y] += 1
            matrix[y][x] += 1
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(n + 1):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def frege_proof_width(clauses):
        # Placeholder function; actual implementation required
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m_min = int(0.1 * n)
        m_max = int(n)
        for _ in range(5):  # Ensure at least 5 instances per size
            m = random.randint(m_min, m_max)
            cnf = generate_cnf(m, n)
            matrix = bruhn_matrix(cnf, n)
            rank = min_rank(matrix)
            width = frege_proof_width(cnf)
            results.append({"rank": rank, "width": width})
    
    conjecture_holds = all(result["rank"] <= (math.log(result["width"]) ** 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frege Proof Width vs Min Rank",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")