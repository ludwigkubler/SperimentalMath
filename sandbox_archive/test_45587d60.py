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
    
    def generate_k_cnf(n, k):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for _ in range(k * n):
            clause = random.sample(literals, k)
            while len(set(clause)) != k:
                clause = random.sample(literals, k)
            clauses.append(clause)
        return clauses

    def incidence_vector_matrix(clauses):
        n = max(abs(lit) for lit in set().union(*clauses))
        matrix = [[0] * (2*n) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit-1] = 1
                else:
                    matrix[i][-lit-1] = 1
        return matrix

    def p_adic_order(matrix):
        n = len(matrix)
        m = len(matrix[0])
        order = 0
        for i in range(n):
            for j in range(m):
                if matrix[i][j] != 0:
                    order += 1
        return order

    def dpll_search_tree_height(clauses, variables):
        def solve(clause_set, assignment):
            if not clause_set:
                return 0
            unit_clauses = [c for c in clause_set if len(c) == 1]
            if unit_clauses:
                lit = unit_clauses[0][0]
                new_assignment = assignment.copy()
                new_assignment[lit] = True
                new_clause_set = [c for c in clause_set if lit not in c and -lit not in c]
                return 1 + solve(new_clause_set, new_assignment)
            pure_lits = []
            for lit in variables:
                pos_count = sum(1 for c in clause_set if lit in c)
                neg_count = sum(1 for c in clause_set if -lit in c)
                if pos_count == 0 and neg_count > 0:
                    pure_lits.append(lit)
                elif pos_count > 0 and neg_count == 0:
                    pure_lits.append(-lit)
            if not pure_lits:
                return float('inf')
            lit = pure_lits[0]
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            new_clause_set = [c for c in clause_set if lit not in c and -lit not in c]
            return 1 + solve(new_clause_set, new_assignment)
        return solve(clauses, {})

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_k_cnf(n, 3)
            matrix = incidence_vector_matrix(clauses)
            order = p_adic_order(matrix)
            height = dpll_search_tree_height(clauses, list(range(1, n+1)))
            results.append((order, height))

    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")