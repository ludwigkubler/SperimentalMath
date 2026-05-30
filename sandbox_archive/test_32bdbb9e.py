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
    
    def generate_random_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        return cnf
    
    def tree_like_resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        unit_clauses = {clause for clause in clauses if len(clause) == 1}
        
        while unit_clauses:
            lit, _ = unit_clauses.pop()
            new_clauses = []
            for clause in clauses:
                if lit in clause:
                    continue
                if -lit in clause:
                    new_clause = tuple(sorted(set(clause) - {lit}))
                    if len(new_clause) == 1:
                        unit_clauses.add((new_clause[0],))
                    else:
                        new_clauses.append(new_clause)
            clauses.update(new_clauses)
        
        return len(clauses)
    
    def symplectic_form_rank(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            for i, lit in enumerate(clause):
                if i == len(clause) - 1:
                    continue
                j, lit2 = clause[i + 1], -lit
                matrix[abs(lit)][abs(lit2)] += 1
                matrix[abs(lit2)][abs(lit)] += 1
        
        rank = 0
        for i in range(1, n + 1):
            pivot = next((j for j in range(i, n + 1) if matrix[j][i] != 0), None)
            if pivot is None:
                continue
            rank += 1
            for j in range(n + 1):
                matrix[i][j], matrix[pivot][j] = matrix[pivot][j], matrix[i][j]
            for j in range(1, n + 1):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return rank
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_ranks = {x[i]: i for i in range(n)}
        y_ranks = {y[i]: i for i in range(n)}
        x_sorted = sorted(x_ranks.keys())
        y_sorted = sorted(y_ranks.keys())
        
        rank_x = [x_ranks[val] for val in x_sorted]
        rank_y = [y_ranks[val] for val in y_sorted]
        
        n = len(rank_x)
        sum_d1 = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        sum_d2 = sum((rank_x[i] - (i + 1)) ** 2 for i in range(n)) + sum((rank_y[i] - (i + 1)) ** 2 for i in range(n))
        
        rho = 1 - 6 * sum_d1 / sum_d2
        return rho
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    cnf = generate_random_cnf(n, m)
    
    w_phi = tree_like_resolution_width(cnf)
    r_phi = symplectic_form_rank(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w(φ) = 0, cannot compute -r(φ)"
        }
    
    rho = spearman_rank_correlation([-r_phi], [math.log2(w_phi)])
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(rho) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.5) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"rho_threshold_not_met\" first_failing_seed={seeds[results.index(next(r for r in results if abs(r['metric_value']) <= 0.5))]}")
    else:
        print("RESULT: INCONCLUSIVE some_rho_values_none")