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
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Convert Boolean matrix to quadratic form coefficients
    Q = []
    for i in range(n):
        row = [0] * n
        for j in range(n):
            if M[i][j]:
                row[j] += 1
                for k in range(j + 1, n):
                    if M[i][k]:
                        row[k] += 1
        Q.append(row)
    
    # Compute minimal rank of the quadratic form
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = next((i for i in range(rank, m) if A[i][j]), None)
            if i_max is not None:
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(rank + 1, m):
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
                rank += 1
        return rank
    
    min_rank = gaussian_elimination(Q)
    
    # Compute communication complexity for the disjointness problem
    def communication_complexity_disjointness(M):
        def partition(lst, k):
            if len(lst) <= k:
                return [lst]
            result = []
            for i in range(1 << (len(lst) - 1)):
                subset = []
                for j in range(len(lst)):
                    if i & (1 << j):
                        subset.append(lst[j])
                result.append(subset)
            return result
        
        def disjointness_communication(A, B):
            n = len(A)
            partitions_A = partition(A, n // 2)
            partitions_B = partition(B, n // 2)
            min_bits = float('inf')
            for part_A in partitions_A:
                for part_B in partitions_B:
                    if all(a != b for a, b in zip(part_A, part_B)):
                        bits = math.ceil(math.log2(len(part_A) + len(part_B)))
                        if bits < min_bits:
                            min_bits = bits
            return min_bits
        
        A = [row[:n//2] for row in M]
        B = [row[n//2:] for row in M]
        return disjointness_communication(A, B)
    
    comm_complexity = communication_complexity_disjointness(M)
    
    # Correlation and difference
    correlation_coefficient = (min_rank - comm_complexity) / math.sqrt(min_rank**2 + comm_complexity**2)
    mean_difference = abs(min_rank - comm_complexity)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient > 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=support_fraction_too_low")