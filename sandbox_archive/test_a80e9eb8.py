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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_bp_width(f):
        n = len(f)
        width = 1
        for i in range(n):
            if f[i] != f[0]:
                width += 1
        return width
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank:
                    factor = matrix[i][j] / matrix[rank][j]
                    for k in range(n):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_free_probability_space_rank(f, n):
        m = len(f)
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if f[i] == j:
                    A[i][j] = 1
        return gaussian_elimination(A)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    W_f = compute_bp_width(f)
    RankFreeProb_Pf = compute_free_probability_space_rank(f, n)
    
    if W_f == 0:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = RankFreeProb_Pf / math.log(W_f)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": "" if 0.5 <= ratio <= 2 else f"Ratio {ratio} outside [0.5, 2]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_data")
    else:
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 2) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not (0.5 <= r["metric_value"] <= 2)), None)
            print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 2]\" first_failing_seed={first_failing_seed}")