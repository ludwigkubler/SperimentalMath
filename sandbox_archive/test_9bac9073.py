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
    
    def generate_planar_graph(n):
        if n < 3 or n > 40:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(1, n):
            edges.append((0, i))
        for i in range(2, n):
            edges.append((i-1, i))
        edges.append((n-1, 0))
        return vertices, edges
    
    def tseitin_formula(vertices, edges):
        variables = {v: f'x{v}' for v in vertices}
        clauses = []
        for u, v in edges:
            clauses.append([f'-{variables[u]}', f'{variables[v]}'])
            clauses.append([f'{variables[u]}', f'-{variables[v]}'])
            clauses.append([f'-{variables[u]}', f'-{variables[v]}', f'x{u}{v}'])
            clauses.append([f'{variables[u]}', f'{variables[v]}', f'-x{u}{v}'])
        return variables, clauses
    
    def hodge_index(clauses):
        n = len(variables)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            if len(clause) == 2:
                u, v = [abs(int(x[1:])) for x in clause]
                A[u][v] += 1
                A[v][u] += 1
        det = gaussian_elimination(A)
        return det
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return 0
            pivot = matrix[i][i]
            for j in range(n + 1):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix[-1][-1]
    
    def resolution_width(clauses):
        queue = clauses[:]
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                return len(queue)
            literal = random.choice(clause)
            for other_clause in queue:
                if literal in other_clause:
                    new_clause = [x for x in other_clause if x != literal]
                    if not new_clause:
                        return len(queue)
                    if new_clause not in queue:
                        queue.append(new_clause)
        return len(queue)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_min_sum = 0
    w_sum = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_planar_graph(n)
        if not graph:
            continue
        variables, clauses = tseitin_formula(*graph)
        h_min = hodge_index(clauses)
        w = resolution_width(clauses)
        h_min_sum += h_min
        w_sum += w
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "h_min vs w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_min_avg = h_min_sum / instances_tested
    w_avg = w_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(h_min * w for h_min, w in zip([h_min_avg] * instances_tested, [w_avg] * instances_tested)) -
                               h_min_sum * w_sum) / math.sqrt((instances_tested * sum(h_min ** 2 for h_min in [h_min_avg] * instances_tested) - h_min_sum ** 2) *
                                                            (instances_tested * sum(w ** 2 for w in [w_avg] * instances_tested) - w_sum ** 2))
    
    return {
        "metric_name": "h_min vs w",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")