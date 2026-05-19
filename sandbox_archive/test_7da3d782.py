# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def power_method(matrix, max_iter=100):
        n = len(matrix)
        v = [Fraction(1, n)] * n  # Initial vector
        for _ in range(max_iter):
            v_next = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm = sum(x**2 for x in v_next)
            if norm == 0:
                break
            v_next = [x / Fraction(norm, n) for x in v_next]
        return max(v_next)

    def frobenius_norm(matrix):
        return math.sqrt(sum(sum(x**2 for x in row) for row in matrix))

    def generate_erdos_renyi_graph(n, p):
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clauses.append([-literals[i], literals[j]])
                    clauses.append([-literals[j], literals[i]])
        return clauses

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if not any(l in c for l in new_assignment)], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if not any(l in c for l in new_assignment)], new_assignment):
                return True
        else:
            literal = next((l for l in literals if l not in assignment), None)
            if dpll(clauses, {**assignment, literal: True}):
                return True
            if dpll(clauses, {**assignment, literal: False}):
                return True
        return False

    n = 40
    p = Fraction(1, 2)
    adj_matrix = generate_erdos_renyi_graph(n, p)
    lambda_2 = power_method(adj_matrix)
    
    if lambda_2 <= 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "lambda_2_not_positive"
        }
    
    tseitin_clauses = tseitin_formula(adj_matrix)
    refutation_length = len(tseitin_clauses) if dpll(tseitin_clauses, {}) else 0
    
    return {
        "metric_name": "resolution_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2**(lambda_2 * n),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")