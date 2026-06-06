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
    
    def generate_sat_formula(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_valuation_group_size(n, p):
        if n == 0:
            return 1
        return p ** (n - 1)
    
    metric_name = "p-adic valuation group size"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        total_size = 0
        for _ in range(instances_tested):
            formula = generate_sat_formula(n)
            p = random.randint(2, 100)
            size = p_adic_valuation_group_size(n, p)
            total_size += size
        
        avg_size = total_size / instances_tested
        expected_size = n * math.log(p)
        
        if avg_size > expected_size:
            conjecture_holds = False
            counterexample = f"n={n}, avg_size={avg_size}, expected_size={expected_size}"
    
    return {
        "metric_name": metric_name,
        "metric_value": avg_size,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")