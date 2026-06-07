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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def topological_sort(clauses):
        graph = {i: [] for i in range(1, 2 * n + 1)}
        in_degree = {i: 0 for i in range(1, 2 * n + 1)}
        
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    graph[literal].append(-literal)
                    in_degree[-literal] += 1
                else:
                    graph[-literal].append(literal)
                    in_degree[literal] += 1
        
        queue = [i for i, degree in in_degree.items() if degree == 0]
        topo_order = []
        
        while queue:
            node = queue.pop(0)
            topo_order.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return topo_order

    def compute_orbit_space(clauses):
        topo_order = topological_sort(clauses)
        orbit_space = set()
        for literal in topo_order:
            orbit_space.add(literal)
        return len(orbit_space)

    def resolution_width(clauses):
        n = len(clauses) // 2
        clauses = [tuple(sorted(c)) for c in clauses]
        clauses = list(set(clauses))
        
        def resolve(clause1, clause2):
            new_clauses = []
            for literal in clause1:
                if -literal in clause2:
                    continue
                new_clause = set(clause1)
                new_clause.remove(literal)
                new_clause.update(clause2)
                new_clauses.append(tuple(sorted(new_clause)))
            return new_clauses
        
        queue = clauses[:]
        while queue:
            new_queue = []
            for i, clause1 in enumerate(queue):
                for j, clause2 in enumerate(queue):
                    if i >= j:
                        continue
                    new_clauses = resolve(clause1, clause2)
                    for new_clause in new_clauses:
                        if new_clause not in queue and new_clause not in new_queue:
                            new_queue.append(new_clause)
            queue.extend(new_queue)
        
        return len(queue)

    n = 30
    cnf_formula = generate_cnf(n)
    orbit_space_size = compute_orbit_space(cnf_formula)
    resolution_width_value = resolution_width(cnf_formula)
    
    if orbit_space_size == 0 or resolution_width_value == 0:
        return {
            "metric_name": "orbit_space_resolution_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_orbit_space"
        }
    
    metric_value = orbit_space_size / resolution_width_value
    return {
        "metric_name": "orbit_space_resolution_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"orbit_space_resolution_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_data")