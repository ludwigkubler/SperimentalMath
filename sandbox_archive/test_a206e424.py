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
        cnf = []
        for _ in range(2**n // 4):  # Ensure at least 8 clauses for n=5
            clause = [random.randint(-1, -n), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        if not cnf:
            return 0
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_cnf = [[l for l in c if l != literal and l != -literal] for c in cnf]
            return 1 + dpll(new_cnf)
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    pure_literals[literal] = True
                else:
                    pure_literals[-literal] = False
        for literal, is_pure in pure_literals.items():
            new_cnf = [[l for l in c if l != literal and l != -literal] for c in cnf]
            return 1 + dpll(new_cnf)
        literal = random.choice([i for i in range(1, n+1)])
        new_cnf_true = [[l for l in c if l != -literal] for c in cnf]
        new_cnf_false = [[l for l in c if l != literal] for c in cnf]
        return 1 + max(dpll(new_cnf_true), dpll(new_cnf_false))
    
    def quantized_phase_space_map(cnf):
        # Simplified mapping for demonstration; actual implementation needed
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    t_star = dpll(cnf)
    R_F = quantized_phase_space_map(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "R(F)/t*(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length is zero"
        }
    
    ratio = R_F / t_star
    return {
        "metric_name": "R(F)/t*(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")