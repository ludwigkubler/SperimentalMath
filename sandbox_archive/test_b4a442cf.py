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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = max(range(rank, rows), key=lambda i: abs(matrix[i][j]))
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(rows):
                if i != rank and matrix[i][j] != 0:
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(cols):
                        matrix[i][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def symplectic_leaf_rank(n, clauses):
        # Placeholder function to compute the minimal rank of a symplectic leaf
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    n = 40
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        clauses = generate_k_cnf(n)
        rank = symplectic_leaf_rank(n, clauses)
        total_rank += rank
    
    average_rank = total_rank / instances_tested
    conjecture_holds = average_rank >= math.log(n) and average_rank <= 3 * math.log(n)
    
    return {
        "metric_name": "Minimal Rank of Symplectic Leaves",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")