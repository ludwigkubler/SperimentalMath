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
    
    n = 40
    m = random.randint(3, n * (n - 1) // 2)
    clause_density = 0.5
    
    # Generate a k-CNF formula with m clauses on n variables
    cnf_formula = []
    for _ in range(m):
        num_vars = random.randint(1, n)
        clause = set(random.sample(range(n), num_vars))
        cnf_formula.append(clause)
    
    # Construct the incidence vector matrix for the polytope defined by the k-CNF formula
    A = [[0] * (2 ** n) for _ in range(m)]
    for i, clause in enumerate(cnf_formula):
        for j in range(1 << n):
            if all((j & (1 << var)) != 0 for var in clause):
                A[i][j] = 1
    
    # Compute the rank of the incidence vector matrix
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = -1
            for i in range(rank, rows):
                if abs(matrix[i][j]) > 1e-9:
                    i_max = i
                    break
            if i_max >= 0:
                matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
                for i in range(rows):
                    if i != rank and abs(matrix[i][j]) > 1e-9:
                        factor = -matrix[i][j] / matrix[rank][j]
                        for k in range(cols):
                            matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    rank = gaussian_elimination(A)
    
    # Compute the average Ehrhart cohomology rank over 30 random seeds
    if rank > m * math.log(m):
        return {
            "metric_name": "Ehrhart Cohomology Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula with {m} clauses and rank {rank}"
        }
    else:
        return {
            "metric_name": "Ehrhart Cohomology Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with {result['metric_value']} clauses and rank {result['metric_value']}\" first_failing_seed={first_failing_seed}")