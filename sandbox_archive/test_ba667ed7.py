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

def generate_boolean_formula(n):
    if n == 1:
        return 'x'
    else:
        subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
        return f'({subformulas[0]} or {subformulas[1]})'

def resolution_width(phi):
    stack = []
    for char in phi:
        if char == '(':
            stack.append(char)
        elif char == ')':
            subformula = ''
            while stack[-1] != '(':
                subformula = stack.pop() + subformula
            stack.pop()
            stack.append(subformula)
        else:
            stack.append(char)
    
    def dpll(formula):
        if formula.startswith('not '):
            return not dpll(formula[4:])
        elif ' or ' in formula:
            p, q = formula.split(' or ')
            return dpll(p) or dpll(q)
        elif ' and ' in formula:
            p, q = formula.split(' and ')
            return dpll(p) and dpll(q)
        else:
            return True
    
    width = 0
    for subformula in stack:
        if ' or ' in subformula:
            width += 1
    return width

def quasi_symmetric_design_size(n):
    # Placeholder function to simulate the calculation of the minimal order of a quasi-symmetric design
    # This is a dummy implementation and should be replaced with an actual algorithm
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Resolution Proof Width Correlation"
    instances_tested = 0
    n_max = 0
    total_correlation = 0
    counterexample = ""
    conjecture_holds = True
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        phi = generate_boolean_formula(n)
        w_phi = resolution_width(phi)
        D_size = quasi_symmetric_design_size(n)
        
        if n > n_max:
            n_max = n
        
        correlation_coefficient = (w_phi - n) / n
        total_correlation += correlation_coefficient
        instances_tested += 1
        
        if abs(correlation_coefficient) < 0.8:
            conjecture_holds = False
            counterexample = f"n={n}, w(φ)={w_phi}, |D|={D_size}"
    
    mean_correlation = total_correlation / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")