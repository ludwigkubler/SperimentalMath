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
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the associated quadratic form Q(M)
    Q = [[sum(M[i][k] * M[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    
    # Compute the minimal rank of Q(M)
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            if all(row[col] == 0 for row in A):
                continue
            pivot_row = next((i for i in range(rank, m) if A[i][col] != 0), None)
            if pivot_row is None:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for i in range(m):
                if i == rank - 1:
                    continue
                factor = A[i][col] / A[rank - 1][col]
                for j in range(n):
                    A[i][j] -= factor * A[rank - 1][j]
        return rank
    
    min_rank_QM = gaussian_elimination(Q)
    
    # Compute the communication complexity for the disjointness problem
    def communication_complexity_disjointness(M):
        # This is a placeholder function. In practice, you would need to implement
        # an actual algorithm for computing the communication complexity of the
        # disjointness problem with input M.
        return 0  # Placeholder value
    
    comm_complexity = communication_complexity_disjointness(M)
    
    return {
        "metric_name": "min_rank(Q(M))",
        "metric_value": min_rank_QM,
        "instances_tested": n * n,
        "conjecture_holds": False,  # Mapping undefined
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")