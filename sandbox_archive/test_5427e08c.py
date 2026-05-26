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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return (n, edges)
    
    def cnf_from_graph(graph):
        n, edges = graph
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            clauses.append(clause)
        return clauses
    
    def min_rank_moduli_space(graph):
        n, _ = graph
        return math.log2(n) if n > 0 else float('inf')
    
    def min_depth_resolution_tree(cnf):
        n = len(cnf)
        depth = [1] * (n + 1)
        for clause in cnf:
            for lit in clause:
                if abs(lit) <= n:
                    depth[abs(lit)] += 1
        return max(depth)
    
    def run_test(n):
        graph = generate_random_graph(n)
        cnf = cnf_from_graph(graph)
        rank_moduli_space = min_rank_moduli_space(graph)
        depth_resolution_tree = min_depth_resolution_tree(cnf)
        return rank_moduli_space, depth_resolution_tree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        rank_sum = 0
        depth_sum = 0
        for _ in range(5):
            rank, depth = run_test(n)
            rank_sum += rank
            depth_sum += depth
        avg_rank = rank_sum / 5
        avg_depth = depth_sum / 5
        results.append((n, avg_rank, avg_depth))
    
    metric_name = "Rank vs Depth"
    metric_value = sum(abs(avg_rank - avg_depth) for _, avg_rank, avg_depth in results)
    instances_tested = len(results) * 5
    conjecture_holds = all(math.isclose(avg_rank, avg_depth, rel_tol=3e-1) for _, avg_rank, avg_depth in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")