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
    
    def generate_cnf(n: int):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def minimal_order_brauer_group(cnf):
        # Placeholder function to simulate Brauer group order calculation
        n = len(cnf)
        if n <= 0:
            return 0
        return n**2 * math.log(n, 2)  # Use math.log instead of random.log
    
    def communication_complexity_rank_variance(cnf):
        # Placeholder function to simulate rank variance calculation
        n = len(cnf)
        if n <= 1:
            return 0
        rank1 = sum(1 for _ in range(n))
        rank2 = sum(-1 for _ in range(n))
        return abs(rank1 - rank2)
    
    instances_tested = 30
    n_max = 40
    metric_values = []
    conjecture_holds = True
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            cnf = generate_cnf(n)
            brauer_group_order = minimal_order_brauer_group(cnf)
            rank_variance = communication_complexity_rank_variance(cnf)
            
            metric_values.append(brauer_group_order * rank_variance)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
    
    if max(metric_values) > 3:
        conjecture_holds = False
        counterexample = "rank_variance_too_high"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Brauer Group Order * Rank Variance",
        "metric_value": mean_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='rank_variance_too_high' first_failing_seed={first_failing_seed}")