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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def communication_complexity_rank(formula):
        n = len(formula)
        ranks = []
        for perm in itertools.permutations(range(n)):
            rank = sum(1 for i in range(n) if formula[i] == '1' and perm[i] % 2 == 0)
            ranks.append(rank)
        return ranks
    
    def variance(ranks):
        mean = sum(ranks) / len(ranks)
        return sum((x - mean) ** 2 for x in ranks) / len(ranks)
    
    def galois_covers(formula):
        n = len(formula)
        covers = set()
        for i in range(n):
            if formula[i] == '1':
                covers.add(i % 2)
        return len(covers)
    
    n_max = 40
    instances_tested = 30
    total_d = 0
    total_r_var = 0
    
    for _ in range(instances_tested):
        formula = generate_boolean_formula(n_max)
        d = galois_covers(formula)
        r_var = variance(communication_complexity_rank(formula))
        
        if d > 50 or r_var < -20:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"d={d}, r_var={r_var}"
            }
        
        total_d += d
        total_r_var += r_var
    
    mean_d = total_d / instances_tested
    mean_r_var = total_r_var / instances_tested
    correlation = (instances_tested * sum(d * r for d, r in zip([mean_d] * instances_tested, [mean_r_var] * instances_tested)) - instances_tested * mean_d * mean_r_var) / (instances_tested * math.sqrt((sum(d ** 2 for d in [mean_d] * instances_tested) - instances_tested * mean_d ** 2) * (sum(r ** 2 for r in [mean_r_var] * instances_tested) - instances_tested * mean_r_var ** 2)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"d>50 or r_var<-20\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")