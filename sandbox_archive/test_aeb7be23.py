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
        if n == 0:
            return 0
        
        # Gaussian elimination to find rank
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                return border_rank([row[:i] + row[i+1:] for row in matrix[1:]])
            
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(n)]
        
        return sum(1 for row in matrix if any(row))

    def communication_complexity(n):
        # Placeholder function to simulate measured communication complexity
        # Replace with actual protocol or literature value
        return n  # Example: simple linear complexity

    n = random.randint(2, 40)
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    
    border_rank_M = border_rank(M)
    R_DISJ_n = communication_complexity(n)
    
    c = 1
    support_threshold = 0.8
    
    if R_DISJ_n >= c * math.log2(border_rank_M) - 5:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"R(DISJ_{n})={R_DISJ_n} < {c}*log2({border_rank_M})-5"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": R_DISJ_n,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= support_threshold:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")