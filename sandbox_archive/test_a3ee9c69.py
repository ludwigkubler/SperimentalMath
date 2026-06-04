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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals):
            if not cnf:
                return True
            literal = next((l for l in literals if l != 0), None)
            if literal is None:
                return False
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if solve([l for l in literals if l != literal]):
                return True
            if solve([l for l in literals if l != -literal]):
                return True
            return False
        return solve(range(1, 2**len(cnf) + 1))
    
    def hodge_complexity(cnf):
        # Placeholder for Hodge complexity calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hdc = hodge_complexity(cnf)
    proof_length = dpll(cnf)
    
    if proof_length is None:
        return {
            "metric_name": "hdc_vs_dpll",
            "metric_value": math.nan,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver did not terminate"
        }
    
    return {
        "metric_name": "hdc_vs_dpll",
        "metric_value": hdc / proof_length if proof_length > 0 else math.nan,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if not math.isnan(r["metric_value"])]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(math.isnan(v) for v in metric_values):
        print("RESULT: INCONCLUSIVE no_valid_data")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((v - sum(metric_values)/len(metric_values))**2 for v in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed + 1}")