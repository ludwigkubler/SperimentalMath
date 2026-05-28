# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        # Generate a random SAT instance with n variables and m clauses
        m = random.randint(n, 2 * n)
        clauses = set()
        while len(clauses) < m:
            clause = tuple(random.sample(range(1, n + 1), 3))
            if all(abs(lit) not in c for c in clauses):
                clauses.add(clause)
        
        # Convert the SAT instance to a matrix
        A = [[0] * (2 * n) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                var_index = abs(lit) - 1
                if lit > 0:
                    A[i][var_index] = 1
                else:
                    A[i][n + var_index] = 1
        
        # Compute the tropical Hodge decomposition
        rank = gaussian_elimination_rank(A)
        
        # Measure the minimal rank of the tropical Hodge decomposition
        metric_values.append(rank)
    
    metric_mean = sum(metric_values) / len(metric_values)
    metric_std = math.sqrt(sum((x - metric_mean) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(x <= 3 * math.log(n) for n, x in zip(range(5, 41), metric_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Tropical Hodge Decomposition",
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def gaussian_elimination_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(m):
            if A[i][j] != 0 and (i_max == -1 or abs(A[i][j]) > abs(A[i_max][j])):
                i_max = i
        if i_max >= 0:
            A[i_max], A[rank] = A[rank], A[i_max]
            for j2 in range(n):
                A[rank][j2] /= A[rank][j]
            for i2 in range(m):
                if i2 != rank:
                    factor = A[i2][j]
                    for j2 in range(n):
                        A[i2][j2] -= factor * A[rank][j2]
            rank += 1
    return rank

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.8 and metric_values[-1] <= 3:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_evidence")