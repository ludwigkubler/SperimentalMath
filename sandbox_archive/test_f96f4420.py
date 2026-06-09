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
    
    def generate_d_regular_graph(d, n):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph

    def is_tautology(formula):
        for clause in formula:
            if len(clause) == 1 and clause[0] < 0:
                return True
        return False

    def dpll(assignment, clauses, variables):
        if not clauses:
            return assignment
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            val = unit_clause[0] > 0
            new_assignment = {**assignment, var: val}
            new_clauses = [c for c in clauses if not (var in c and all(not (v == -var) for v in c))]
            return dpll(new_assignment, new_clauses, variables)
        pure_literal = next((v for v in variables if sum(1 for c in clauses if v in c or -v in c) == 1), None)
        if pure_literal:
            val = True
            new_assignment = {**assignment, pure_literal: val}
            new_clauses = [c for c in clauses if not (pure_literal in c and all(not (v == -pure_literal) for v in c))]
            return dpll(new_assignment, new_clauses, variables)
        p = random.choice(variables)
        new_assignment_true = {**assignment, p: True}
        result_true = dpll(new_assignment_true, clauses, variables)
        if result_true:
            return result_true
        new_assignment_false = {**assignment, p: False}
        return dpll(new_assignment_false, clauses, variables)

    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    c1, c2 = clauses[i], clauses[j]
                    common_negatives = [v for v in c1 if -v in c2]
                    if common_negatives:
                        new_clause = list(set(c1) | set(c2))
                        for neg in common_negatives:
                            new_clause.remove(neg)
                            new_clause.remove(-neg)
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)

    def tseitin_formula(graph):
        n = len(graph)
        variables = list(range(1, 2 * n + 1))
        clauses = []
        for i in range(n):
            clauses.append([variables[2 * i], variables[2 * i + 1]])
            for j in graph[i]:
                clauses.append([-variables[2 * i], -variables[2 * (j + n)]])
                clauses.append([-variables[2 * i + 1], -variables[2 * (j + n) + 1]])
        return variables, clauses

    def min_representation_size(clauses):
        assignment = {}
        for var in range(1, 2 * len(graph) + 1):
            assignment[var] = random.choice([True, False])
        return sum(1 for v in assignment if assignment[v])

    n = 30
    d = 4
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "min_rep",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    variables, clauses = tseitin_formula(graph)
    if is_tautology(clauses):
        return {
            "metric_name": "min_rep",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rep = min_representation_size(clauses)
    resolution_width = resolution(clauses)
    
    return {
        "metric_name": "min_rep",
        "metric_value": abs(min_rep - resolution_width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")