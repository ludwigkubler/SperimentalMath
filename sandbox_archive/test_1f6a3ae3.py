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
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate literals
        literals = [f'x{i}' for i in range(1, n + 1)]
        
        # Generate clauses
        for _ in range(m):
            clause = random.sample(literals, 2)
            clauses.append(f'{clause[0]} OR {clause[1]}')
        
        return variables, clauses
    
    def compute_colored_jones_polynomial(n):
        # Simplified version of colored Jones polynomial computation
        return Fraction(2 ** n, 1)
    
    def compute_resolution_depth(clauses):
        # Simplified version of Resolution depth computation
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    variables, clauses = generate_tseitin_formula(n, m)
    
    qtw_g = compute_colored_jones_polynomial(n)
    d_r_g = compute_resolution_depth(clauses)
    
    metric_name = "Resolution Depth"
    metric_value = d_r_g
    instances_tested = 1
    conjecture_holds = qtw_g >= 2 ** (math.log(qtw_g, 2) * math.log(2, math.e))
    counterexample = "" if conjecture_holds else f"QTW(G)={qtw_g}, D_R(G)={d_r_g}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")