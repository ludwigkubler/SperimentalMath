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
    
    def generate_instance(n):
        variables = set()
        P = []
        for _ in range(2 * n):
            new_var = random.randint(0, 1000)
            while any(new_var == p[i] for p in P for i in range(len(p))):
                new_var = random.randint(0, 1000)
            variables.add(new_var)
            P.append(tuple(sorted(variables)))
        return list(variables), P
    
    def hodge_index(P):
        n = len(P[0])
        count = [0] * (2 ** n)
        for p in P:
            index = 0
            for i in range(n):
                if p[i]:
                    index |= 1 << i
            count[index] += 1
        return max(count)
    
    def log_square(n):
        return math.log2(n) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        variables, P = generate_instance(n)
        h_index = hodge_index(P)
        expected_bound = log_square(n) * 10  # Adjust constant as needed
        
        if h_index > expected_bound:
            conjecture_holds = False
            counterexample = f"n={n}, Hodge index={h_index} > {expected_bound}"
        
        total_metric_value += h_index
        instances_tested += len(P)
        n_max = max(n_max, n)
    
    return {
        "metric_name": "Hodge Index",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")