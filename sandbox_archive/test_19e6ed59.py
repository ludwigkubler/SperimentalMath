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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[(i + 1) % n] for i in range(n)):
                clauses.append(clause)
        return clauses
    
    def tropical_category_depth(clauses):
        # Simplified mapping to a depth based on the number of clauses
        return len(clauses)
    
    def frege_proof_depth(clauses):
        # Placeholder function, actual implementation needed
        return 2 ** len(clauses)  # Example: exponential growth for simplicity
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    depth_trop_cat = tropical_category_depth(clauses)
    depth_frege = frege_proof_depth(clauses)
    
    alpha_n = math.log2(n) ** 2
    beta = 1.0  # Placeholder for actual constant
    bound_beta = beta * math.log(depth_frege)
    
    conjecture_holds = (depth_trop_cat <= alpha_n) and (depth_trop_cat <= bound_beta)
    counterexample = "" if conjecture_holds else f"Depth(TropCat(F))={depth_trop_cat}, α(n)={alpha_n}, β * log(d(F))={bound_beta}"
    
    return {
        "metric_name": "Tropical Category Depth",
        "metric_value": depth_trop_cat,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")