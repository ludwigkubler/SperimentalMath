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
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            if all(abs(lit) != abs(lit2) for lit, lit2 in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(abs(lit) == abs(lit2) and lit != lit2 for lit in clauses[i] for lit2 in clauses[j]):
                        new_clause = [lit for lit in clauses[i] if lit not in clauses[j]] + [lit for lit in clauses[j] if lit not in clauses[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            clauses.append(new_clause)
            width += 1
        return width
    
    def symplectic_form_rank(cnf):
        n = len(cnf[0])
        A = [[0] * (n+1) for _ in range(n+1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    i, j = lit-1, lit
                else:
                    i, j = -lit-1, -lit
                A[i][j] += 1
                A[j][i] += 1
        rank = 0
        for row in A:
            if any(x != 0 for x in row):
                rank += 1
                for other_row in A:
                    if any(other_row[x] != 0 for x in range(n+1)):
                        factor = other_row[i] / row[i]
                        for k in range(n+1):
                            other_row[k] -= factor * row[k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        rank = symplectic_form_rank(cnf)
        results.append((n, width, rank))
    
    if not results:
        return {
            "metric_name": "Spearman correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "Spearman correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    widths = [w for _, w, _ in results]
    ranks = [-r for _, _, r in results]
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {x: i+1 for i, x in enumerate(sorted(set(x)))}
        rank_y = {y: i+1 for i, y in enumerate(sorted(set(y)))}
        sum_diff_squared = sum((rank_x[x] - rank_y[y])**2 for x, y in zip(x, y))
        return 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
    
    correlation = spearman_correlation(widths, ranks)
    
    return {
        "metric_name": "Spearman correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")