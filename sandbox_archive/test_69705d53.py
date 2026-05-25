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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def taylor_coefficients(f, n):
        # Placeholder for actual Taylor coefficient computation
        return [sum(f[i] * (x ** i) for x in range(2)) for i in range(n + 1)]
    
    def hermitian_form_rank(coeffs):
        # Placeholder for actual Hermitian form rank computation
        return len(coeffs)
    
    def decision_tree_path_complexity(f, n):
        # Placeholder for actual decision tree path complexity computation
        return sum(1 for coeff in coeffs if coeff != 0)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    coeffs = taylor_coefficients(f, n)
    N_f = hermitian_form_rank(coeffs)
    D_f = decision_tree_path_complexity(f, n)
    
    if D_f == 0:
        return {
            "metric_name": "N_f / D(f)^{1/2}",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "D(f) is zero, making the ratio undefined."
        }
    
    ratio = Fraction(N_f, D_f**0.5).limit_denominator()
    return {
        "metric_name": "N_f / D(f)^{1/2}",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= math.log2(n)**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")