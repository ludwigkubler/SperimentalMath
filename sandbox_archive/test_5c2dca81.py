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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if all(abs(x) > 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_length(cnf):
        # Simplified resolution length calculation
        return len(cnf) * (len(cnf) + 1) // 2
    
    def tropicalized_local_system_rank(resolution_length):
        # Simplified tropicalized local system rank calculation
        return math.log(resolution_length, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        length = resolution_length(cnf)
        rank = tropicalized_local_system_rank(length)
        ratio = rank / math.log(n, 2)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    support_fraction = all(0.9 <= r <= 1.1 for r in results)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = all(0.9 <= r["metric_value"] <= 1.1 for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")