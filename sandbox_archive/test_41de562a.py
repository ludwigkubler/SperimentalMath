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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tropical_polynomial(f):
        return [f(x) for x in range(2**len(f))]
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        cc = float('inf')
        for i in range(n):
            f_i = lambda x: f(x ^ (1 << i))
            cc_i = communication_complexity(f_i)
            if cc_i < cc:
                cc = cc_i
        return cc + 1
    
    def tropical_cycle_rank(t_f):
        n = len(t_f)
        if n == 0:
            return 0
        rank = 1
        for i in range(n):
            t_f_i = [t_f[j] ^ t_f[i] for j in range(n)]
            rank_i = tropical_cycle_rank(t_f_i)
            if rank_i > rank:
                rank = rank_i
        return rank
    
    def boolean_function(n):
        return random.choices([0, 1], k=n)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        f = boolean_function(n)
        cc_r_f = communication_complexity(f)
        t_f = tropical_polynomial(f)
        tr_t_f = tropical_cycle_rank(t_f)
        
        instances_tested += 1
        total_metric_value += tr_t_f
        
        if tr_t_f > 2**cc_r_f:
            conjecture_holds = False
            counterexample = f"CC_R(f)={cc_r_f}, TR(t_f)={tr_t_f}"
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in range(instances_tested))) / instances_tested
    
    return {
        "metric_name": "tropical_cycle_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")