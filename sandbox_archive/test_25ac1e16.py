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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        lit = unit_clause[0]
        if lit in assignment and assignment[lit] != (lit > 0):
            return False
        return dpll([c for c in cnf if lit not in c], {**assignment, lit: True})
    pure_literal = next((l for l in range(1, n + 1) if all(l not in c or -l not in c for c in cnf)), None)
    if pure_literal:
        return dpll([c for c in cnf if pure_literal not in c], {**assignment, pure_literal: True})
    lit = random.choice(cnf[0])
    return dpll(cnf + [[-lit]], {**assignment, lit: True}) or dpll(cnf + [[-lit]], {**assignment, lit: False})

def quasi_frobenius_rank(cnf):
    n = len(set(abs(lit) for lit in cnf))
    if n == 0:
        return 0
    rank = 0
    while True:
        assignment = {}
        for lit in range(1, n + 1):
            if random.choice([True, False]):
                assignment[lit] = True
            else:
                assignment[-lit] = True
        if dpll(cnf, assignment):
            rank += 1
        else:
            return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    proof_widths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * 2))
            rank = quasi_frobenius_rank(cnf)
            min_ranks.append(rank)
            proof_widths.append(len(dpll(cnf)))
    
    if not min_ranks or not proof_widths:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": 0.0,
            "instances_tested": len(min_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(proof_widths) / len(proof_widths)
    covariance = sum((min_ranks[i] - mean_rank) * (proof_widths[i] - mean_width) for i in range(len(min_ranks))) / len(min_ranks)
    variance_rank = sum((min_ranks[i] - mean_rank) ** 2 for i in range(len(min_ranks))) / len(min_ranks)
    variance_width = sum((proof_widths[i] - mean_width) ** 2 for i in range(len(proof_widths))) / len(proof_widths)
    correlation_coefficient = covariance / (math.sqrt(variance_rank) * math.sqrt(variance_width))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")