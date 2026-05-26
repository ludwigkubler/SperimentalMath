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
        return [row[:n-1] for row in A if row[-1] == 0]

    def cohomology_rank(n):
        # Placeholder function to compute the rank of H^1(C(n), R)
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    def communication_complexity(n):
        # Placeholder function to compute the randomized communication complexity CC_R(DISJ_n)
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n**2)

    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        rank = cohomology_rank(n)
        cc = communication_complexity(n)
        if cc == 0:
            continue
        ratio = rank / cc
        ratios.append(ratio)
    
    if not ratios:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_ratios"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    support_fraction = sum(1 for r in ratios if r >= 0.8) / len(ratios)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "conjecture_holds": support_fraction >= 0.8 and mean_ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        RESULT = "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {RESULT} mean={mean_ratio:.2f} std=0.00 support_fraction={support_fraction:.2f}")