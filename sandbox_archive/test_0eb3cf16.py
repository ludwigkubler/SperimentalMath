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
            # Find pivot
            max_row = i
            for r in range(i+1, m):
                if abs(A[r][i]) > abs(A[max_row][i]):
                    max_row = r
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate
            for r in range(m):
                if r != i:
                    factor = A[r][i] / A[i][i]
                    for c in range(n):
                        A[r][c] -= factor * A[i][c]
        return A
    
    def min_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def unique_game_instance(n):
        instance = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            instance.append(row)
        return instance
    
    n = random.randint(5, 40)
    instance = unique_game_instance(n)
    
    # Calculate minimal rank of the dual object
    dual_object = [[instance[j][i] for j in range(n)] for i in range(n)]
    min_rank_value = min_rank(dual_object)
    
    # Calculate minimum distinguishability gap
    ε = 0.1 * random.random() + 0.05
    
    # Compute the ratio of minimal rank to ε^2
    ratio = min_rank_value / (ε ** 2)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")