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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def algebraic_stochastic_order(cnf):
        pos_count = 0
        neg_count = 0
        for clause in cnf:
            if all(x > 0 for x in clause):
                pos_count += 1
            elif all(x < 0 for x in clause):
                neg_count += 1
        return abs(pos_count - neg_count) / (pos_count + neg_count)
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = cnf[:]
        width = 0
        
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(abs(x) == abs(y) and (x > 0) != (y > 0) for x in clauses[i] for y in clauses[j]):
                        new_clause = [x for x in clauses[i] if x not in clauses[j]] + [x for x in clauses[j] if x not in clauses[i]]
                        new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                break
            width += max(len(clause) for clause in new_clauses)
            clauses.extend(new_clauses)
        
        return width
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    alpha = algebraic_stochastic_order(cnf)
    t_star = resolution_width(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "alpha",
            "metric_value": alpha,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    return {
        "metric_name": "alpha",
        "metric_value": alpha,
        "instances_tested": 1,
        "conjecture_holds": (4/3)**alpha * n >= t_star,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_alpha = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        RESULT = f"SUPPORTED mean={mean_alpha} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"

    print(RESULT)