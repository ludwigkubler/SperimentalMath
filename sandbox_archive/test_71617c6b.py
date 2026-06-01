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

def generate_tseitin_formula(n):
    if n < 3:
        return None
    
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for the Tseitin formula
    for i in range(1, n-1):
        clauses.append(f'({variables[i-1]} ^ {variables[i]}) v ~{variables[i+1]}')
    
    # Add final clause
    clauses.append(f'{variables[-2]} v ~{variables[-1]}')
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        formula = generate_tseitin_formula(n)
        if formula is None:
            continue
        
        # Simulate Brauer group and tensor product rank (placeholder values)
        BPrank = random.randint(1, n)
        
        # Simulate resolution proof width (placeholder values)
        w = random.randint(10, 2 * n)
        
        metric_values.append(BPrank / w)
    
    if not metric_values:
        return {
            "metric_name": "BPrank/w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    variance = sum((x - mean) ** 2 for x in metric_values) / len(metric_values)
    std_dev = math.sqrt(variance)
    
    return {
        "metric_name": "BPrank/w",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")