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
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        clauses = []
        for _ in range(k * n):
            clause = random.sample(literals, k)
            if len(set(clause)) == k:
                clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses, n):
        m = len(clauses)
        A = [[0] * (2 * n) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    A[i][lit - 1] = 1
                else:
                    A[i][-lit - 1] = 1
        return A
    
    def p_adic_order(matrix):
        m, n = len(matrix), len(matrix[0])
        max_entry = max(abs(x) for row in matrix for x in row)
        if max_entry == 0:
            return 0
        p = 2
        while True:
            found_nonzero = False
            for i in range(m):
                for j in range(n):
                    if abs(matrix[i][j]) % p != 0:
                        matrix[i][j] //= p
                        found_nonzero = True
            if not found_nonzero:
                return int(math.log(max_entry, p))
    
    def dpll_search_tree_height(clauses):
        def solve(clauses, assignment):
            if len(clauses) == 0:
                return 1
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                lit = unit_clause[0]
                new_assignment = assignment + [lit] if lit > 0 else assignment + [-lit]
                return solve([c for c in clauses if lit not in c and -lit not in c], new_assignment)
            pure_literal = next((i for i in range(1, n + 1) if (i not in assignment and -i not in assignment)), None)
            if pure_literal is not None:
                new_assignment = assignment + [pure_literal]
                return solve([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
            lit, _ = random.choice(clauses)
            return solve(clauses, assignment + [lit]) + solve(clauses, assignment + [-lit])
        return solve(clauses, [])
    
    n_values = [5, 10, 15, 20, 30, 40]
    p = 2
    metrics = []
    
    for n in n_values:
        clauses = generate_k_cnf(n, 3)
        A = incidence_matrix(clauses, n)
        order = p_adic_order(A)
        height = dpll_search_tree_height(clauses)
        metrics.append((order, height))
    
    if len(metrics) < 100:
        return {
            "metric_name": "p-adic Order vs DPLL Height",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n for n in n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    order_values = [m[0] for m in metrics]
    height_values = [m[1] for m in metrics]
    mean_order = sum(order_values) / len(order_values)
    mean_height = sum(height_values) / len(height_values)
    correlation = sum((order - mean_order) * (height - mean_height) for order, height in metrics) / len(metrics)
    
    return {
        "metric_name": "p-adic Order vs DPLL Height",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")