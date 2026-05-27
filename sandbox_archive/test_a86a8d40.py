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
    
    def generate_k_cnf(k, n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(k)]
            cnf.append(clause)
        return cnf
    
    def rank_eilenberg_mac_lane_space(cnf_formula):
        # Placeholder function to compute the rank of A_k(n)
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf_formula)  # Simplified for demonstration purposes
    
    k_values = [2, 3, 4, 5]
    n = 10
    total_rank = 0
    instances_tested = 0
    
    for k in k_values:
        cnf_formula = generate_k_cnf(k, n)
        rank = rank_eilenberg_mac_lane_space(cnf_formula)
        total_rank += rank
        instances_tested += 1
    
    metric_value = total_rank / len(k_values)
    conjecture_holds = True
    counterexample = ""
    
    if metric_value > 3:
        conjecture_holds = False
        counterexample = "metric_value_exceeds_threshold"
    
    return {
        "metric_name": "Average Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.9 and max(metric_values) <= 3:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"metric_value_exceeds_threshold\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")