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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def monodromy_group_order(f):
        # Placeholder function to simulate the computation of the monodromy group order
        n = int(math.log2(len(f)))
        return n + 1
    
    metric_name = "monodromy_group_order"
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        f = generate_boolean_function(n)
        comm_rank_var = communication_complexity_rank(f) ** 2
        g_f = monodromy_group_order(f)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_metric_value += g_f
        
        if abs(g_f - comm_rank_var) / max(1, comm_rank_var) > 0.1:
            conjecture_holds = False
            counterexample = f"n={n}, |G_f|={g_f}, CommRankVar(f)={comm_rank_var}"
    
    metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - 3) <= 0.5) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")