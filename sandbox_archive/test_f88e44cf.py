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
    
    def compute_minimal_genus(graph):
        n = len(graph)
        if n == 0:
            return 0
        genus = (n - sum(len(neighbors) for neighbors in graph) // 2 + 1) // 2
        return max(0, genus)
    
    def generate_tseitin_formula(graph):
        n = len(graph)
        literals = list(range(-n, 0))
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(literals[j])
            clauses.append(clause)
            for j in range(i + 1, n):
                if j not in graph[i]:
                    clause = [-literals[i], -literals[j]]
                    clauses.append(clause)
        return literals, clauses
    
    def compute_resolution_proof_width(literals, clauses):
        stack = []
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            stack.append((literal[0], True))
            for clause in clauses:
                if literal[0] in clause:
                    clause.remove(literal[0])
                    if len(clause) == 1:
                        unit_clauses.append(clause)
        return len(stack)
    
    n_max = 40
    instances_tested = 0
    correlation_sum = 0.0
    min_genus_list = []
    proof_width_list = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(2, n - 1)
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            instances_tested += 1
            min_genus = compute_minimal_genus(graph)
            literals, clauses = generate_tseitin_formula(graph)
            proof_width = compute_resolution_proof_width(literals, clauses)
            min_genus_list.append(min_genus)
            proof_width_list.append(proof_width)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = sum((min_genus - mean_min_genus) * (proof_width - mean_proof_width)
                      for min_genus, proof_width in zip(min_genus_list, proof_width_list)) / instances_tested
    mean_min_genus = sum(min_genus_list) / instances_tested
    mean_proof_width = sum(proof_width_list) / instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.9 and all(0.7 <= corr < 1.0 for corr in min_genus_list),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + list(range(50, 80))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(0.7 <= corr < 1.0 for r in results for corr in min_genus_list):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_correlation")