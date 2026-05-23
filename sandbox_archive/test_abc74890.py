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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if A[i][i] == 0:
            for j in range(i+1, m):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue
        pivot = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = -A[j][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    return sum(1 for row in A if any(row))

def communication_complexity(G):
    n = len(G)
    subsets = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                subsets[i].add(j)
                subsets[j].add(i)
    
    def min_bits(subsets):
        bits = []
        while any(subsets):
            bit = 0
            for i in range(n):
                if subsets[i]:
                    bit |= (1 << i)
                    for j in subsets[i]:
                        subsets[j].discard(j)
            bits.append(bit)
        return len(bits)
    
    return min_bits(subsets)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    config_space = lambda G: [[G[j][k] for k in range(n)] for j in range(n)]
    rank = gaussian_elimination(config_space(G))
    comm_complexity = communication_complexity(G)
    
    if comm_complexity == 0:
        return {
            "metric_name": "rank_to_comm_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_zero"
        }
    
    ratio = Fraction(rank, comm_complexity)
    return {
        "metric_name": "rank_to_comm_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
        print(f"{RESULT} mean={mean_ratio:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] == "communication_complexity_zero" for r in results):
        print("RESULT: FALSIFIED counterexample=\"communication_complexity_zero\" first_failing_seed=" + str(seeds[results.index(next((r for r in results if r["counterexample"] == "communication_complexity_zero"), None))]))
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation_or_tautological_inequality")