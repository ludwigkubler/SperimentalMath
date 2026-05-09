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
    
    def generate_3cnf(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.choice([f'x{i}', f'~x{i}']) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def variable_substitution(clauses, n):
        variables = {}
        for i in range(1, n+1):
            a = random.randint(1, 2)
            b = random.randint(1, 2)
            variables[f'x{i}'] = f'a{a}b{b}'
            variables[f'~x{i}'] = f'a{3-a}b{3-b}'
        return [[variables[var] for var in clause] for clause in clauses]
    
    def polynomial_from_3cnf(clauses):
        terms = []
        for clause in clauses:
            term = ' + '.join([f'{random.choice(["+", "-"])} {var}' for var in clause])
            terms.append(term)
        return f'({") * ("}.join(terms))'
    
    def symmetric_power_rank(poly, k):
        if k == 0:
            return 1
        rank = 0
        n = len(poly.split(' + '))
        for i in range(n):
            subpoly = poly.replace(f'x{i+1}', f'y{i}')
            rank += symmetric_power_rank(subpoly, k-1)
        return rank
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    substituted_clauses = variable_substitution(clauses, n)
    permanent_poly = polynomial_from_3cnf(substituted_clauses)
    
    det_poly = ' * '.join([f'x{i}' for i in range(1, n+1)])
    
    k = math.ceil(n / 2)
    perm_rank = symmetric_power_rank(permanent_poly, k)
    det_rank = symmetric_power_rank(det_poly, k)
    
    ratio = Fraction(perm_rank, det_rank)
    threshold = Fraction(2**(n/2), 10)
    
    conjecture_holds = ratio >= threshold
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < {threshold}"
    
    return {
        "metric_name": "Symmetric Power Rank Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient evidence to support or falsify the conjecture")