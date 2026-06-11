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
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        
        for i in range(n):
            clauses.append([literals[2 * i], literals[2 * i + 1]])
            for j in graph[i]:
                if j < i:
                    continue
                clauses.append([-literals[2 * i], literals[2 * j + 1]])
                clauses.append([-literals[2 * i + 1], literals[2 * j]])
        
        return literals, clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses)
        polynomial = [0] * (n + 1)
        polynomial[0] = 1
        for clause in clauses:
            new_poly = [0] * (n + 1)
            for literal in clause:
                if literal > 0:
                    for i in range(n, -1, -1):
                        new_poly[i] += polynomial[i - literal]
                else:
                    for i in range(n, -1, -1):
                        new_poly[i] -= polynomial[i + abs(literal)]
            polynomial = [x % 2 for x in new_poly]
        return polynomial
    
    def hodge_theoretic_generators(polynomial):
        n = len(polynomial)
        generators = set()
        for i in range(n):
            if polynomial[i]:
                generators.add(i)
        return len(generators)
    
    def frege_proof_depth(clauses):
        n = len(clauses)
        depth = [0] * (n + 1)
        stack = []
        for clause in clauses:
            max_depth = 0
            for literal in clause:
                if literal > 0:
                    max_depth = max(max_depth, depth[literal - 1])
                else:
                    max_depth = max(max_depth, depth[-literal - 1] + 1)
            stack.append((max_depth + 1, clause))
        while stack:
            current_depth, current_clause = stack.pop()
            for literal in current_clause:
                if literal > 0:
                    depth[literal - 1] = current_depth
                else:
                    depth[-literal - 1] = current_depth - 1
            max_depth = 0
            for literal in current_clause:
                if literal > 0:
                    max_depth = max(max_depth, depth[literal - 1])
                else:
                    max_depth = max(max_depth, depth[-literal - 1] + 1)
            stack.append((max_depth + 1, current_clause))
        return depth[n]
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    n_max = 40
    instances_tested = 30
    h_values = []
    f_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4)):
            graph = generate_d_regular_graph(n, n - 2)
            if not graph:
                continue
            literals, clauses = tseitin_formula(graph)
            polynomial = clause_indicator_polynomial(clauses)
            h_value = hodge_theoretic_generators(polynomial)
            f_value = frege_proof_depth(clauses)
            h_values.append(h_value)
            f_values.append(f_value)
    
    if not h_values or not f_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = pearson_correlation(h_values, f_values)
    p_value = 2 * (1 - math.fabs(correlation)) if abs(correlation) < 1 else 0
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.9 and p_value <= 0.05,
        "counterexample": "" if correlation >= 0.9 else f"correlation={correlation}, p-value={p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")