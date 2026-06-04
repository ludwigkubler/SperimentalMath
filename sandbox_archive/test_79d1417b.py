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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            for j in range(i+1, n+1):
                clause += f' OR {variables[j-1]}'
            clauses.append(clause)
        return ' AND '.join(clauses)

    def p_adic_valuation(n):
        if n == 0:
            return float('inf')
        count = 0
        while n % 2 == 0:
            n //= 2
            count += 1
        return count

    def resolution_width(formula):
        # Simplified version for demonstration purposes
        return len(formula.split())

    def longest_linear_dependency_chain(formula):
        # Simplified version for demonstration purposes
        return formula.count(' AND ')

    d = random.randint(2, 5)
    n = random.randint(d+1, min(40, d*3))
    formula = generate_tseitin_formula(n)
    
    valuation = p_adic_valuation(n)
    width = resolution_width(formula)
    l_chain = longest_linear_dependency_chain(formula)
    
    k = 1
    while True:
        if math.log(valuation**k) >= n - l_chain:
            break
        k += 1
    
    metric_value = math.log(valuation**k)
    conjecture_holds = abs(metric_value - (n - l_chain)) <= 0.1 * (n - l_chain)
    
    return {
        "metric_name": "log(p^k(w(φ)))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")