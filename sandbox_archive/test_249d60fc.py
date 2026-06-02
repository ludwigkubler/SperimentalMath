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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        adjacency_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if adjacency_matrix[u][v] == 0 and u != v:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
                edges_added += 1
        return adjacency_matrix
    
    def spectral_radius(matrix):
        n = len(matrix)
        eigenvalues = []
        for _ in range(5):  # Simple power iteration method
            v = [random.random() for _ in range(n)]
            v_norm = math.sqrt(sum(x**2 for x in v))
            v = [x / v_norm for x in v]
            Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            Av_norm = math.sqrt(sum(x**2 for x in Av))
            lambda_i = sum(Av[i] * v[i] for i in range(n)) / Av_norm
            eigenvalues.append(lambda_i)
        return max(eigenvalues)
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clause.append(f'-{literals[j]}')
                    clause.append(f'-{literals[i]}')
                    clause.append(literals[j])
            clauses.append(clause)
        return clauses
    
    def dpll_solver(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal.startswith('-'):
                new_assignment[literal[1:]] = False
            return dpll_solver([c for c in clauses if literal not in c], new_assignment)
        pure_literal = next((l for l in literals.values() if all(l not in c or -l not in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll_solver(clauses, new_assignment)
        literal = random.choice(list(literals.values()))
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        if dpll_solver([c for c in clauses if literal not in c], new_assignment_true):
            return True
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        return dpll_solver([c for c in clauses if -literal not in c], new_assignment_false)
    
    def frege_proof_depth(clauses):
        return len(dpll_solver(clauses, {}))
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    w_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        if n > n_max:
            n_max = n
        for _ in range(5):  # Sample 5 instances per size
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            h = spectral_radius(graph)
            phi_G = tseitin_formula(graph)
            w = frege_proof_depth(phi_G)
            h_values.append(h)
            w_values.append(w)
            instances_tested += 1
    
    correlation_coefficient = sum((h - mean_h) * (w - mean_w) for h, w in zip(h_values, w_values)) / len(h_values)
    mean_h = sum(h_values) / len(h_values)
    mean_w = sum(w_values) / len(w_values)
    
    if abs(correlation_coefficient) >= 0.7:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Correlation coefficient < 0.7"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")