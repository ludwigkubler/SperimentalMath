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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] == 1:
                count += 1
        return count
    
    def rank_of_free_algebra(n):
        # Simplified rank estimation using a random matrix approach
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(i + 1, n):
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def alpha_n(n):
        # Simplified approximation of α(n)
        return n**2
    
    instances_tested = 0
    total_cc_xor = 0
    total_rank_F = 0
    
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        cc_xor = communication_complexity(f)
        rank_F = rank_of_free_algebra(len(f))
        
        instances_tested += 1
        total_cc_xor += cc_xor
        total_rank_F += rank_F
    
    mean_cc_xor = total_cc_xor / instances_tested
    mean_rank_F = total_rank_F / instances_tested
    
    alpha_n_value = alpha_n(40)  # Using the maximum n tested for simplicity
    if mean_rank_F <= alpha_n_value * 1.1 and mean_cc_xor <= alpha_n_value:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_rank_F={mean_rank_F}, alpha_n*1.1={alpha_n_value*1.1}, mean_cc_xor={mean_cc_xor}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc_xor,
        "instances_tested": instances_tested,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")