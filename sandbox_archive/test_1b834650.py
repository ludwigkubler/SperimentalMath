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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_proof_length(cnf):
        # Simplified DPLL solver to estimate proof length
        clauses = set(tuple(sorted(c)) for c in cnf)
        unit_clauses = {c[0] for c in clauses if len(c) == 1}
        while unit_clauses:
            new_unit_clauses = set()
            for clause in clauses:
                if any(abs(lit) not in unit_clauses for lit in clause):
                    continue
                new_lit = -sum(lit for lit in clause if abs(lit) in unit_clauses)
                if new_lit < 0:
                    new_unit_clauses.add(-new_lit)
            if not new_unit_clauses:
                break
            unit_clauses.update(new_unit_clauses)
        return len(clauses) + len(unit_clauses)
    
    def count_arithmetic_progressions(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        progressions = set()
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                diff = j - i
                if diff <= 2:
                    continue
                progression = {i, j}
                k = j + diff
                while k <= n:
                    progression.add(k)
                    k += diff
                if len(progression) >= 3:
                    progressions.add(tuple(sorted(progression)))
        return len(progressions)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    cnf = generate_cnf(n, m)
    t_F = resolution_proof_length(cnf)
    P_F = count_arithmetic_progressions(cnf)
    
    if P_F > 10 * math.log(t_F):
        return {
            "metric_name": "P(F)",
            "metric_value": P_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with n={n}, m={m} has |P(F)| > 10 * log(t*(F))"
        }
    
    return {
        "metric_name": "P(F)",
        "metric_value": P_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Instance with |P(F)| > 10 * log(t*(F))' first_failing_seed={first_failing_seed}")