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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
        for u in range(n):
            for v in range(u+1, n):
                if v not in graph[u] and u not in graph[v]:
                    clauses.append([f'-{literals[u]}', f'-{literals[v]}'])
        return literals, clauses
    
    def frege_proof_depth(clauses):
        stack = []
        for clause in clauses:
            if all('-' + var in stack or var in stack for var in clause):
                continue
            for var in clause:
                if '-' + var in stack:
                    stack.remove('-' + var)
                else:
                    stack.append(var)
        return len(stack)
    
    def local_zeta_function_order(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph.values())
        return degree_sum / (n * (n - 1))
    
    d_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    n_max = 0
    total_lzf = 0
    total_depth = 0
    
    for d in d_values:
        for _ in range(5):
            graph = generate_d_regular_graph(d * 2, d)
            if graph is None:
                continue
            instances_tested += 1
            n_max = max(n_max, len(graph))
            literals, clauses = tseitin_formula(graph)
            depth = frege_proof_depth(clauses)
            lzf = local_zeta_function_order(graph)
            total_lzf += lzf
            total_depth += depth
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_lzf = total_lzf / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(lzf * depth for lzf, depth in zip([mean_lzf] * instances_tested, [mean_depth] * instances_tested)) - 
                               sum([mean_lzf] * instances_tested) * sum([mean_depth] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(lzf**2 for lzf in [mean_lzf] * instances_tested) - (sum([mean_lzf] * instances_tested))**2) *
                                        (instances_tested * sum(depth**2 for depth in [mean_depth] * instances_tested) - (sum([mean_depth] * instances_tested))**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")