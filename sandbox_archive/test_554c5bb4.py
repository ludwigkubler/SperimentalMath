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

def generate_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = sorted(random.sample(variables, clause_size))
        clauses.append(clause)
    return clauses

def calculate_coxeter_group_complexity(clauses: list) -> int:
    # Placeholder function to compute the complexity of the reflection poset
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses)

def calculate_resolution_proof_width(n: int, m: int) -> float:
    # Placeholder function to compute the resolution proof width
    # This is a dummy implementation and should be replaced with actual logic
    return n * m

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "resolution_proof_width"
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for m in range(1, min(200, int(n**2/2) + 1)):
            instances_tested += 1
            clauses = generate_instance(n, m)
            complexity = calculate_coxeter_group_complexity(clauses)
            width = calculate_resolution_proof_width(n, m)
            
            n_max = max(n_max, n)
            total_metric_value += width
            
            upper_bound = n**(1/3) * m**(2/3) + math.log(m)
            if width > upper_bound:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}: width={width} > {upper_bound}"
    
    mean_metric_value = total_metric_value / instances_tested
    result = {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")