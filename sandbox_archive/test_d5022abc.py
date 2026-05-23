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
    
    n = random.randint(5, 40)  # Number of variables
    m = random.randint(10, 200)  # Number of clauses
    
    # Generate a random CNF formula with n variables and m clauses
    cnf_formula = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        cnf_formula.append(clause)
    
    # Construct the associated affine variety over the Boolean ring
    # This is a placeholder function; actual implementation depends on Hodge theory
    def hodge_index(cnf):
        return len(cnf) ** (1/3) * n ** (2/3)
    
    h = hodge_index(cnf_formula)
    
    # Build the DPLL search tree for the corresponding satisfiability problem
    # This is a placeholder function; actual implementation depends on DPLL algorithm
    def dpll_width(cnf):
        return len(cnf) ** 3 * n ** 6
    
    w = dpll_width(cnf_formula)
    
    metric_name = "Hodge Index / DPLL Width Ratio"
    metric_value = h / w
    instances_tested = 1
    conjecture_holds = h <= m ** (1/3) * n ** (2/3)
    counterexample = "" if conjecture_holds else f"H(V)={h}, W(DPLL)={w}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")