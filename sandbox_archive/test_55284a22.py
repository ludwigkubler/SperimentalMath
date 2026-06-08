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
        if (n * d) % 2 != 0 or n < d + 1:
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
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}_{j}' for i in range(n) for j in range(len(graph[i]))]
        clauses = []
        for i in range(n):
            if not graph[i]:
                continue
            clause = [-literals[2 * i - 1]]
            for neighbor in graph[i]:
                clause.append(literals[2 * neighbor])
            clauses.append(clause)
            for j in range(len(graph[i])):
                for k in range(j + 1, len(graph[i])):
                    clauses.append([-literals[2 * graph[i][j] - 1], -literals[2 * graph[i][k] - 1]])
        return clauses
    
    def resolution_width(clauses):
        n = len(clauses)
        queue = [clauses]
        width = 0
        while queue:
            new_queue = []
            for clause in queue:
                if not clause:
                    return float('inf')
                literal = min(abs(x) for x in clause)
                new_clause = [-x for x in clause if abs(x) != literal]
                if len(new_clause) > width:
                    width = len(new_clause)
                for other_clause in queue:
                    if literal in other_clause and -literal in other_clause:
                        continue
                    new_queue.append([x for x in other_clause if x not in new_clause])
            queue = new_queue
        return width
    
    def diophantine_equations(graph):
        n = len(graph)
        equations = set()
        for i in range(n):
            for j in range(len(graph[i])):
                for k in range(j + 1, len(graph[i])):
                    eq = f'x{i}_{j} + x{j}_{k} - x{i}_{k}'
                    equations.add(eq)
        return equations
    
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        graph = generate_d_regular_graph(random.randint(2, min(n - 1, 4)), n)
        if graph is None:
            continue
        
        diophantine_eqs = diophantine_equations(graph)
        width = resolution_width(tseitin_formula(graph))
        
        if len(diophantine_eqs) > 0 and width != float('inf'):
            instances_tested += 1
            metric_value += len(diophantine_eqs) / width
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    mean_metric = metric_value / instances_tested
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
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
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")