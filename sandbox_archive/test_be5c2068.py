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

def random_cnf(n, m):
    literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def dpll_width(cnf):
    def dpll(model, clauses):
        unit_clauses = [c for c in clauses if len(c) == 1 and c[0] not in model]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_model = model.copy()
            new_model[literal] = True
            if dpll(new_model, [c for c in clauses if literal not in c]):
                return True
            new_model[literal] = False
            if dpll(new_model, [c for c in clauses if -literal not in c]):
                return True
        else:
            empty_clause = any(all(lit not in model and -lit not in model for lit in c) for c in clauses)
            if empty_clause:
                return False
            pure_literals = {}
            for lit in set.union(*clauses):
                pos_count, neg_count = 0, 0
                for clause in clauses:
                    if lit in clause:
                        pos_count += 1
                    elif -lit in clause:
                        neg_count += 1
                if pos_count == 0 or neg_count == 0:
                    pure_literals[lit] = pos_count > 0
            if not pure_literals:
                return True
            literal, value = random.choice(list(pure_literals.items()))
            new_model = model.copy()
            new_model[literal] = value
            if dpll(new_model, clauses):
                return True
        return False

    return len(dpll({}, cnf))

def tropical_symplectic_form(cnf):
    n = len(cnf)
    M = [[0 for _ in range(n)] for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                i, j = lit - 1, (lit + 1) % n
            else:
                i, j = -(lit + 1), lit % n
            M[i][j] += 1
    return sum(sum(row) for row in M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = random_cnf(n, n * (n - 1) // 2)
        omega = tropical_symplectic_form(cnf)
        w = dpll_width(cnf)
        results.append((omega, w))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values[:len(results)]),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    omega_values = [omega for omega, _ in results]
    w_values = [w for _, w in results]
    
    mean_omega = sum(omega_values) / len(omega_values)
    mean_w = sum(w_values) / len(w_values)
    
    correlation = 0
    for i in range(len(results)):
        correlation += (omega_values[i] - mean_omega) * (w_values[i] - mean_w)
    correlation /= math.sqrt(sum((x - mean_omega) ** 2 for x in omega_values)) * math.sqrt(sum((y - mean_w) ** 2 for y in w_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values[:len(results)]),
        "conjecture_holds": abs(correlation) >= 0.7 and abs(mean_omega - mean_w) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation\" first_failing_seed={first_failing_seed}")