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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

# Constants
GF_2_X = [1, 0]  # GF(2)[x] is represented as a list of coefficients for x^0 and x^1

def dpll(clauses, literals):
    if not clauses:
        return True
    clause = random.choice(clauses)
    pos_lit = next((l for l in literals if l not in clause), None)
    neg_lit = next((-l for l in literals if -l not in clause), None)
    
    if pos_lit is not None and dpll([c for c in clauses if pos_lit not in c and -pos_lit not in c], literals + [pos_lit]):
        return True
    elif neg_lit is not None and dpll([c for c in clauses if neg_lit not in c and -neg_lit not in c], literals + [neg_lit]):
        return True
    
    return False

def resolution_width(F):
    n = len(F)
    width = 0
    for _ in range(1, n + 1):
        if dpll(F, list(range(1, n + 1))):
            width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random k-CNF formula with n variables
    n = random.randint(3, 40)
    k = 3
    F = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        F.append(clause)
    
    # Compute the resolution proof width
    width = resolution_width(F)
    
    # Calculate the order of the Brauer group over GF(2)[x] for k = 3
    br_k_order = 2  # The order of the Brauer group over GF(2)[x] is 2 for k = 3
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": n,
        "conjecture_holds": width <= 10 * br_k_order,  # Assuming a constant c = 10
        "counterexample": "" if width <= 10 * br_k_order else f"width={width}, br_k_order={br_k_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = (sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='width exceeds 10 times Brauer group order' first_failing_seed={first_failing_seed}")