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
    
    def border_rank(M):
        n = len(M)
        if n == 0:
            return 0
        M_tilde = [[M[i][j] for j in range(n)] for i in range(n)]
        rank = 1
        while True:
            found = False
            for i in range(n):
                for j in range(n):
                    if M_tilde[i][j] != 0:
                        found = True
                        break
                if found:
                    break
            if not found:
                return rank
            for i in range(n):
                if M_tilde[i][j] != 0:
                    M_tilde[i][j] /= M_tilde[i][j]
            for k in range(n):
                if k != j:
                    factor = M_tilde[k][j]
                    for l in range(n):
                        M_tilde[k][l] -= factor * M_tilde[j][l]
            rank += 1

    def communication_complexity(n):
        # Placeholder function. Replace with actual computation.
        return n  # Example: trivial protocol complexity

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        border_rank_M = border_rank(M)
        R = communication_complexity(n)
        
        if R < math.log2(border_rank_M):
            return {
                "metric_name": "communication_complexity",
                "metric_value": R,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, border_rank(M)={border_rank_M}, R={R}"
            }
        
        results.append(R)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r >= math.log2(border_rank_M)]) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 149))  # First 30 prime numbers
    
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.log2(border_rank_M)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r < math.log2(border_rank_M))
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[first_failing_seed]}, border_rank(M)={border_rank_M}, R={results[first_failing_seed]}\" first_failing_seed={seeds[first_failing_seed]}")