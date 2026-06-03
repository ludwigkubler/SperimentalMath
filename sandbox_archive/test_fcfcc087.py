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
    
    def generate_boolean_function(n):
        return [random.choice([True, False]) for _ in range(2**n)]
    
    def zonotope_vertices(f):
        n = len(f)
        vertices = []
        for i in range(1 << n):
            vertex = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    vertex[j] = 1
            vertices.append(vertex)
        return vertices
    
    def ehrhart_polynomial(vertices):
        n = len(vertices[0])
        d = len(vertices)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        c = [0] * n
        
        for i in range(d):
            for j in range(n):
                A[j][j] += vertices[i][j]
                b[j] += vertices[i][j]
        
        for j in range(n):
            c[j] = -b[j] / d
        
        return c
    
    def communication_matrix_rank(f):
        n = len(f)
        tree = [[] for _ in range(2 * n)]
        queue = [0]
        while queue:
            node = queue.pop()
            if node >= n:
                continue
            left = 2 * node + 1
            right = 2 * node + 2
            tree[node].append(left)
            tree[node].append(right)
            queue.append(left)
            queue.append(right)
        
        rank = 0
        visited = [False] * (2 * n)
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if visited[node]:
                        continue
                    visited[node] = True
                    for neighbor in tree[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
                rank += 1
        
        return rank
    
    def degree_of_polynomial(poly):
        return len(poly) - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        vertices = zonotope_vertices(f)
        poly = ehrhart_polynomial(vertices)
        deg = degree_of_polynomial(poly)
        R_f = communication_matrix_rank(f)
        
        if deg == 0 or R_f == 0:
            continue
        
        results.append({
            "n": n,
            "deg": deg,
            "R_f": R_f
        })
    
    if not results:
        return {
            "metric_name": "communication_matrix_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    deg_sum = sum(result["deg"] for result in results)
    R_f_sum = sum(result["R_f"] for result in results)
    mean_deg = deg_sum / instances_tested
    mean_R_f = R_f_sum / instances_tested
    
    if abs(mean_R_f - mean_deg) > 10:
        return {
            "metric_name": "communication_matrix_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"R(f) = {mean_R_f}, deg(EhrhartPolynomial(Zonotope(f))) = {mean_deg}"
        }
    
    return {
        "metric_name": "communication_matrix_rank",
        "metric_value": mean_R_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    conjecture_holds_count = sum(1 for result in results if result["conjecture_holds"])
    
    mean_metric_value = sum(metric_values) / len(metric_values) if metric_values else None
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values)) if metric_values else None
    
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='R(f) does not match deg(EhrhartPolynomial(Zonotope(f)))' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")