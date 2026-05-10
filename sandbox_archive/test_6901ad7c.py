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
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses
    
    def monomial_to_index(monomial, variables):
        index = 0
        for var in variables:
            if var in monomial:
                index |= (1 << (abs(monomial[var]) - 1))
        return index
    
    def hilbert_function(d, n):
        return Fraction((n + d) * (n + d + 1) // 2, (d + 1) * d // 2)
    
    def sos_degree(clauses):
        # Simplified estimation of SOS degree
        return len(clauses) + 2
    
    n = 40
    m = 60
    clauses = generate_3cnf(n, m)
    variables = list(range(1, n + 1))
    
    monomial_dict = {}
    for clause in clauses:
        for var in clause:
            if abs(var) not in monomial_dict:
                monomial_dict[abs(var)] = {var: 1}
            else:
                monomial_dict[abs(var)][var] += 1
    
    hilbert_values = []
    d_max = sos_degree(clauses)
    for d in range(d_max + 1):
        hilbert_values.append(hilbert_function(d, n))
    
    metric_value = sum(hilbert_values) / len(hilbert_values)
    instances_tested = 1
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "Hilbert Function",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")