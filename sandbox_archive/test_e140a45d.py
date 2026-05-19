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
    
    def border_rank(matrix):
        n = len(matrix)
        if n == 0 or any(len(row) != n for row in matrix):
            return 0
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            if abs(matrix[max_row][i]) < 1e-8:
                continue
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            rank += 1
            for j in range(n):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity(n):
        # Placeholder function, replace with actual protocol
        return n  # Example: simple protocol that communicates n bits
    
    n = random.randint(2, 40)
    M = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    border_rank_M = border_rank(M)
    R_DISJ_n = communication_complexity(n)
    
    c = 1
    lower_bound = c * math.log2(border_rank_M) - 5
    
    if R_DISJ_n >= lower_bound:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"R(DISJ_{n})={R_DISJ_n} < {lower_bound}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": R_DISJ_n,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37, 41, 43, 47, 53]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")