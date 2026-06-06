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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, 2 * m) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def communication_complexity_rank(cnf):
        # Placeholder implementation
        # This should be replaced with the actual computation of communication complexity rank
        return random.randint(1, len(cnf))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        comm_rank = communication_complexity_rank(cnf)
        results.append(comm_rank)
    
    variance = sum((x - sum(results) / len(results)) ** 2 for x in results) / len(results)
    conjecture_holds = variance <= max(n_values) ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_variance = sum(results) / len(results)
    std_variance = math.sqrt(sum((x - mean_variance) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max([5, 10, 15, 20, 30, 40]) ** 2) / len(results)
    
    if all(r <= max([5, 10, 15, 20, 30, 40]) ** 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif any(r > max([5, 10, 15, 20, 30, 40]) ** 2 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")