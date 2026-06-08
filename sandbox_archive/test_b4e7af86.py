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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_number_field(cnf):
        # Simplified mapping to a number field
        n = len(cnf[0])
        return (n, sum(len(clause) for clause in cnf))
    
    def hodge_arakelov_index(number_field):
        n, d = number_field
        return Fraction(n * d, 2)
    
    def frege_proof_depth(cnf):
        # Simplified mapping to proof depth
        n = len(cnf[0])
        return n + len(cnf)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        number_field = cnf_to_number_field(cnf)
        
        ai = hodge_arakelov_index(number_field)
        d = frege_proof_depth(cnf)
        
        if ai > 10 or d > 10:
            return {
                "metric_name": "Pearson correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "AI(K(φ)) or d(φ) exceeds 10"
            }
        
        results.append((ai, d))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "AI(K(φ)) or d(φ) exceeds 10"
        }
    
    ai_values, d_values = zip(*results)
    mean_ai = sum(ai_values) / len(ai_values)
    mean_d = sum(d_values) / len(d_values)
    correlation = (sum((ai - mean_ai) * (d - mean_d) for ai, d in results) /
                   math.sqrt(sum((ai - mean_ai)**2 for ai in ai_values) *
                             sum((d - mean_d)**2 for d in d_values)))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": correlation > 0.7,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")