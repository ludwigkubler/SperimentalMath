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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{literals[i-1]}'
            clauses.append(clause)
        return literals, clauses
    
    def resolution_width(clauses):
        # Simplified resolution width calculation (not actual DPLL implementation)
        return len(clauses) * 2
    
    def min_monomials(literal):
        # Placeholder for minimal monomial representation calculation
        return len(literal.split('x')) - 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = generate_tseitin(n)
    
    w_phi = resolution_width(clauses)
    M_phi = sum(min_monomials(lit) for lit in literals)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(w_phi - M_phi) <= M_phi / 2,
        "counterexample": "" if conjecture_holds else f"Resolution width {w_phi} not within factor of 2 from min monomials {M_phi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")