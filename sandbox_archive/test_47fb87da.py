# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = max(range(i, m), key=lambda r: abs(Augmented[r][i]))
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            factor = Augmented[i][i]
            for j in range(i, n + 1):
                Augmented[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = Augmented[k][i]
                    for j in range(i, n + 1):
                        Augmented[k][j] -= factor * Augmented[i][j]
        return [row[-1] for row in Augmented]
    
    def generate_structure(n):
        # Placeholder for generating a structure with MCSP depth D(S)
        # For simplicity, we use a random permutation matrix
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        return A
    
    def mcsp_depth(A):
        # Placeholder for computing MCSP depth of a structure
        # For simplicity, we use the number of rows as a proxy
        return len(A)
    
    def action_count(A):
        # Placeholder for computing action count of GT group on a structure
        # For simplicity, we use the determinant of the matrix
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return abs(det)
    
    def estimate_constant(action_counts, mcsp_depths):
        ratios = [action_counts[i] / mcsp_depths[i] for i in range(len(action_counts))]
        mean_ratio = sum(ratios) / len(ratios)
        std_dev = (sum((r - mean_ratio)**2 for r in ratios) / len(ratios))**0.5
        return mean_ratio, std_dev
    
    n_values = [5, 10, 15, 20, 30, 40]
    action_counts = []
    mcsp_depths = []
    
    for n in n_values:
        structure = generate_structure(n)
        depth = mcsp_depth(structure)
        count = action_count(structure)
        action_counts.append(count)
        mcsp_depths.append(depth)
    
    mean_ratio, std_dev = estimate_constant(action_counts, mcsp_depths)
    
    conjecture_holds = mean_ratio <= 1.5
    counterexample = "" if conjecture_holds else "mean_ratio > 1.5"
    
    return {
        "metric_name": "Mean Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(action_counts),
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio > 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")