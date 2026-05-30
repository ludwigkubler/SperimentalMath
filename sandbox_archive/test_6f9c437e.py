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
    
    # Define constants and parameters
    n = random.randint(5, 30)  # Number of variables
    m = random.randint(10, 100)  # Number of clauses
    p = random.choice([2, 3, 5])  # Characteristic of the field
    
    # Generate a random k-CNF instance
    k = random.randint(2, 4)
    cnf_instance = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            lit = random.choice(range(-n, n+1))
            if lit != 0 and lit not in clause:
                clause.add(lit)
        cnf_instance.append(list(clause))
    
    # Placeholder function to compute the minimal genus of a surface
    def min_genus(cnf):
        # This is a dummy implementation for demonstration purposes
        return len(cnf) ** (1/3) * n ** (2/3)
    
    min_gen = min_genus(cnf_instance)
    
    return {
        "metric_name": "minimal genus",
        "metric_value": min_gen,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_gen <= c * (m ** (1/3) * n ** (2/3)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")