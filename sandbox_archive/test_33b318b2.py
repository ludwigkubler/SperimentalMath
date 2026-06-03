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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f'x{i}', f'~x{i}'])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'~x{i}', f'~x{j}', f'x{i}|x{j}'])
        return literals, clauses
    
    def quadratic_form(literals, clauses):
        n = len(literals)
        Q = [[0] * n for _ in range(n)]
        for clause in clauses:
            if len(clause) == 2 and clause[1].startswith('~'):
                i = int(clause[1][2:]) - 1
                Q[i][i] += 1
            elif len(clause) == 3:
                i, j = [int(lit[2:]) - 1 for lit in clause if not lit.startswith('~')]
                Q[i][j] -= 1
                Q[j][i] -= 1
        return Q
    
    def min_rank(Q):
        n = len(Q)
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if Q[j][i]), None)
            if pivot is not None:
                rank += 1
                for j in range(n):
                    Q[i][j], Q[pivot][j] = Q[pivot][j], Q[i][j]
                for k in range(n):
                    if k != i:
                        factor = -Q[k][i] / Q[i][i]
                        for j in range(n):
                            Q[k][j] += factor * Q[i][j]
        return rank
    
    def resolution_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            if len(clause) > width:
                width = len(clause)
        return width
    
    results = []
    for n in range(5, 41):
        literals, clauses = tseitin_formula(n)
        Q = quadratic_form(literals, clauses)
        min_rank_Q = min_rank(Q)
        w_phi_G = resolution_width(clauses)
        results.append((min_rank_Q, w_phi_G))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    min_rank_values = [r[0] for r in results]
    w_phi_G_values = [r[1] for r in results]
    
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    mean_w_phi_G = sum(w_phi_G_values) / len(w_phi_G_values)
    
    correlation_coefficient = (sum((min_rank_values[i] - mean_min_rank) * (w_phi_G_values[i] - mean_w_phi_G) for i in range(len(results))) /
                               math.sqrt(sum((min_rank_values[i] - mean_min_rank)**2 for i in range(len(results))) *
                                         sum((w_phi_G_values[i] - mean_w_phi_G)**2 for i in range(len(results)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient > 0.9 and abs(correlation_coefficient - 1) < 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient < 0.9 or abs(correlation_coefficient - 1) >= 2"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)