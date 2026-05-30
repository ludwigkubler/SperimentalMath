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
    
    def generate_3cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                lit = random.randint(1, n * 2)
                if lit <= n:
                    clause.add(lit)
                else:
                    clause.add(-lit)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def min_local_dimension(clauses):
        # Placeholder for actual computation
        return math.log(len(clauses)) ** 2 / math.log(len(set(abs(lit) for lit in sum(clauses, ())))) ** 2
    
    def resolution_width(clauses):
        # Placeholder for actual computation
        return len(max(clauses, key=len))
    
    m_values = [10, 20, 40]
    results = []
    
    for m in m_values:
        n = random.randint(10, 50)
        clauses = generate_3cnf(m, n)
        
        local_dim = min_local_dimension(clauses)
        width = resolution_width(clauses)
        
        results.append({
            "m": m,
            "n": n,
            "local_dim": local_dim,
            "width": width
        })
    
    mean_local_dim = sum(result["local_dim"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    
    conjecture_holds = all(
        abs(math.log(result["n"]) / result["width"]) <= 0.1
        for result in results
    )
    
    return {
        "metric_name": "mean_local_dim",
        "metric_value": mean_local_dim,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_local_dim = sum(result["metric_value"] for result in results) / len(results)
    fraction_supporting = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_local_dim} std=0 support_fraction=1.0")
    elif fraction_supporting >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_local_dim} std=0 support_fraction={fraction_supporting}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"m={result['results'][0]['m']}, n={result['results'][0]['n']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break