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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            return float('inf')
        
        # Simple heuristic: count the number of unique rows
        rows = set()
        for i in range(n + 1):
            row = [f[j] for j in range(2**i, min(2**(i+1), len(f)))]
            rows.add(tuple(row))
        
        return len(rows)
    
    def minimal_geometric_entanglement(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            return float('inf')
        
        # Simple heuristic: count the number of unique pairs
        pairs = set()
        for i in range(n + 1):
            for j in range(2**i, min(2**(i+1), len(f))):
                for k in range(j + 1, min(2**(i+1), len(f))):
                    pair = (f[j], f[k])
                    pairs.add(tuple(pair))
        
        return len(pairs)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        ccr_f = communication_complexity_rank(f)
        mge_f = minimal_geometric_entanglement(f)
        
        if ccr_f == float('inf') or mge_f == float('inf'):
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        total_metric_value += mge_f / ccr_f
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_metric_value >= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mge_over_ccr",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")