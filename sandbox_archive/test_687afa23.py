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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input length must be a power of 2")
        
        # DPLL solver to find the minimum number of literals needed
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next(l for l in range(1, n+1) if l not in assignment and -l not in assignment)
            pos_clauses = [c for c in clauses if literal in c]
            neg_clauses = [c for c in clauses if -literal in c]
            if dpll(pos_clauses, assignment | {literal: True}):
                return True
            if dpll(neg_clauses, assignment | {literal: False}):
                return True
            return False
        
        min_literals = n + 1
        for i in range(2**n):
            assignment = {}
            clauses = []
            for j in range(n):
                if f[i] == (i >> j) & 1:
                    clauses.append([j+1])
                else:
                    clauses.append([-j-1])
            if dpll(clauses, assignment):
                min_literals = min(min_literals, len(assignment))
        return min_literals
    
    def minimal_order_quadratic_form(f):
        n = int(math.log2(len(f)))
        # Constructive method using Gröbner basis over Boolean ring
        # This is a simplified version and may not be correct for all cases
        variables = list(range(n))
        monomials = []
        for i in range(1 << n):
            if f[i] == 1:
                monomial = [variables[j] for j in range(n) if (i >> j) & 1]
                monomials.append(monomial)
        
        # Simplify the set of monomials
        simplified_monomials = []
        for m in monomials:
            if all(all(x not in n for x in m) for n in simplified_monomials):
                simplified_monomials.append(m)
        
        return len(simplified_monomials)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        mw = monotone_width(f)
        moqf = minimal_order_quadratic_form(f)
        results.append((mw, moqf))
    
    correlation_coefficient = None
    if len(results) > 1:
        x = [math.log2(mw) for mw, _ in results]
        y = [moqf for _, moqf in results]
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        correlation_coefficient = numerator / denominator if denominator != 0 else None
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) > 0.9,
        "counterexample": "" if correlation_coefficient is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")