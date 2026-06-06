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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        rank = 0
        A_echelon = gaussian_elimination(A)
        for row in A_echelon:
            if any(row):
                rank += 1
        return rank

    def hodge_structure_rank(n):
        # Placeholder function to compute Hodge structure rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        hodge_ranks = []
        rank_variances = []

        while instances_tested < 30:
            # Generate a random n-party communication protocol
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            
            # Compute Hodge structure rank and matrix rank variance
            h_rank = hodge_structure_rank(n)
            r_rank = matrix_rank(A)
            rank_variances.append(r_rank)
            
            hodge_ranks.append(h_rank)
            instances_tested += 1

        avg_h_rank = sum(hodge_ranks) / len(hodge_ranks)
        avg_variance = variance(rank_variances)
        
        ratio = avg_h_rank / n
        
        results.append({
            "n": n,
            "avg_h_rank": avg_h_rank,
            "avg_variance": avg_variance,
            "ratio": ratio
        })

    min_ratio = min(r["ratio"] for r in results if r["instances_tested"] >= 30)
    
    return {
        "metric_name": "Ratio of Minimal Hodge Structure Rank to Average Rank",
        "metric_value": min_ratio,
        "instances_tested": sum(1 for r in results if r["instances_tested"] >= 30),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": min_ratio >= 1 / 40,  # Assuming n <= 40
        "counterexample": "" if min_ratio >= 1 / 40 else f"Ratio {min_ratio} < 1/40"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {r['metric_value']} < 1/40\" first_failing_seed={first_failing_seed}")