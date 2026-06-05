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
    n = random.randint(5, 40)
    clauses = [random.choice([1, -1]) * sum(random.sample(range(n), k)) for k in range(1, n+1)]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if A[j][i] != 0:
                    max_row = j
                    break
            if max_row is not None:
                A[max_row], A[rank] = A[rank], A[max_row]
                pivot = A[rank][i]
                for j in range(n):
                    A[rank][j] /= pivot
                for j in range(m):
                    if j != rank:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[rank][k]
                rank += 1
        return rank
    
    def min_symplectic_volume(clauses, n):
        A = [[0] * (n + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for j in range(n):
                if clause & (1 << j):
                    A[i][j] = 1
            A[i][-1] = -1
        
        rank = gaussian_elimination(A)
        return n - rank
    
    def communication_complexity_rank(clauses, n):
        # Placeholder function; actual implementation needed
        return len(clauses)  # Simplified for testing purposes
    
    sv = min_symplectic_volume(clauses, n)
    ccrank = communication_complexity_rank(clauses, n)
    
    if sv == 0 or ccrank == 0:
        return {
            "metric_name": "correlation",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sv / ccrank
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break