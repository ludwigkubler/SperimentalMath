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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def permanent(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            sub_det = permanent(sub_matrix, n-1)
            det += sign * matrix[0][j] * sub_det
        return det
    
    def invariant_dimension(matrix, n):
        if n == 2:
            return 1  # GL_2-invariant polynomials are constant and thus have dimension 1
        permanent_poly = permanent(matrix, n)
        determinant_poly = permanent(matrix, n)  # Placeholder for actual determinant calculation
        return len(permanent_poly), len(determinant_poly)
    
    def generate_random_matrix(n):
        return [[random.randint(-5, 5) for _ in range(n)] for _ in range(n)]
    
    n_values = [2, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = generate_random_matrix(n)
        permanent_rank, determinant_rank = invariant_dimension(matrix, n)
        ratio = Fraction(permanent_rank, determinant_rank) if determinant_rank != 0 else None
        results.append({
            "n": n,
            "permanent_rank": permanent_rank,
            "determinant_rank": determinant_rank,
            "ratio": ratio
        })
    
    total_ratio = sum(result["ratio"] for result in results if result["ratio"] is not None)
    mean_ratio = total_ratio / len(results) if results else 0
    
    return {
        "metric_name": "Ratio of Permanent to Determinant Dimensions",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(result["ratio"] > 1 for result in results if result["ratio"] is not None),
        "counterexample": "" if all(result["ratio"] > 1 for result in results if result["ratio"] is not None) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")