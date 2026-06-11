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
    
    def generate_sat_instance(n):
        literals = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clause = [random.choice(literals), -random.choice(literals)]
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        variables = set()
        new_vars = {}
        for i, clause in enumerate(clauses):
            var = f'v{i+1}'
            variables.add(var)
            new_vars[clause] = var
        formula = []
        for clause in clauses:
            if len(clause) == 2:
                a, b = clause
                formula.append([a, -new_vars[(a, b)]])
                formula.append([-a, new_vars[(a, b)]])
                formula.append([-b, new_vars[(a, b)]])
                formula.append([b, -new_vars[(a, b)]])
            else:
                raise ValueError("Clause must have exactly two literals")
        return variables, formula
    
    def resolution_proof_width(formula):
        queue = formula[:]
        while True:
            unit_clauses = [c for c in queue if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = unit_clauses[0]
            queue.remove(unit_clause)
            for clause in queue:
                if -unit_clause[0] in clause:
                    new_clause = [l for l in clause if l != -unit_clause[0]]
                    if len(new_clause) == 1:
                        return len(queue) + 1
                    queue.append(new_clause)
        return len(queue)
    
    def groupoid_cospans(variables, formula):
        cospans = {}
        for var in variables:
            cospans[var] = ([], [])
        for clause in formula:
            a, b = clause
            if -a in cospans[b][0]:
                cospans[a][1].append(b)
            else:
                cospans[a][0].append(-b)
            if -b in cospans[a][0]:
                cospans[b][1].append(a)
            else:
                cospans[b][0].append(-a)
        return cospans
    
    def minimal_index(cospans):
        indices = []
        for var, (in_edges, out_edges) in cospans.items():
            index = 0
            visited = set()
            stack = [var]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    index += len(in_edges[node]) + len(out_edges[node])
                    for neighbor in in_edges[node] + out_edges[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
            indices.append(index)
        return sum(indices) / len(indices)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        sat_instance = generate_sat_instance(n)
        variables, formula = tseitin_formula(sat_instance)
        width = resolution_proof_width(formula)
        cospans = groupoid_cospans(variables, formula)
        index = minimal_index(cospans)
        
        metric_values.append(index)
        if len(metric_values) > 1:
            corr = pearson_correlation(metric_values[:-1], [width] * (len(metric_values) - 1))
            if corr < 0.6:
                conjecture_holds = False
                counterexample = f"Correlation {corr} below threshold for n={n}"
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation(metric_values, [resolution_proof_width(tseitin_formula(generate_sat_instance(n)))[1] for _ in range(instances_tested)]),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample='Correlation below threshold' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")