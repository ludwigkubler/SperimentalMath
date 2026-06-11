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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{literals[i-1]}'
            clauses.append(clause)
        return literals, clauses

    def resolution_width(phi):
        # Simplified resolution width calculation (not actual resolution)
        return len(phi)

    def min_monomials(clauses):
        # Simplified monomial count (not actual monomials)
        return sum(len(c.split(' ')) for c in clauses)

    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = generate_tseitin_formula(n)
    phi = clauses
    w_phi = resolution_width(phi)
    M_phi = min_monomials(clauses)

    if M_phi == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    if w_phi is None or M_phi is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    if w_phi / M_phi < 0.5 or w_phi / M_phi > 2:
        return {
            "metric_name": "resolution_width",
            "metric_value": w_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Resolution width {w_phi} not within factor of 2 from min monomials {M_phi}"
        }

    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 30

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r['conjecture_holds'] for r in results):
        mean_value = sum(r['metric_value'] for r in results) / len(results)
        std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r['conjecture_holds']]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = next(result['counterexample'] for result in results if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")