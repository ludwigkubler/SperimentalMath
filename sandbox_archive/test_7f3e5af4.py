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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals):
            if not cnf:
                return literals
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                return solve(literals + [literal])
            
            p = random.choice([l for l in range(1, n+1) if l not in literals and -l not in literals])
            new_cnf_true = [c for c in cnf if p not in c and -p not in c]
            new_cnf_false = [c for c in cnf if -p not in c and p not in c]
            
            result_true = solve(literals + [p])
            if result_true is not None:
                return result_true
            else:
                return solve(literals + [-p])
        
        n = len(cnf[0]) // 2
        return solve([])
    
    def hdc(cnf):
        # Placeholder for Hodge decomposition complexity calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    hdc_value = hdc(cnf)
    proof_length = dpll(cnf)
    
    if proof_length is None:
        return {
            "metric_name": "hdc_vs_dpll",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver did not terminate"
        }
    
    return {
        "metric_name": "hdc_vs_dpll",
        "metric_value": hdc_value / proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")