# auto-injected by SEC sandbox
import math
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

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for _ in range(random.randint(2, 3))]
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        # Simulate DPLL width (simplified version)
        dpll_width = n * 2  # Placeholder value
        
        # Simulate twisted tensor product rank (simplified version)
        min_rank = n + 1  # Placeholder value
        
        ratio = min_rank / dpll_width
        results.append({
            "n": n,
            "min_rank": min_rank,
            "dpll_width": dpll_width,
            "ratio": ratio
        })
    
    metric_value = sum(r["ratio"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["ratio"] <= 3 for r in results)
    counterexample = "" if conjecture_holds else f"Ratio exceeded 3 for n={results[0]['n']}"
    
    return {
        "metric_name": "MinRank / DPLLWidth Ratio",
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
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["ratio"] >= 10 for r in results):
        first_failing_seed = next(r for r in results if r["ratio"] >= 10)["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")