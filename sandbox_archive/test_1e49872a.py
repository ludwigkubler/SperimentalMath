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
    
    def is_k_clique(graph, k):
        n = len(graph)
        for i in range(n):
            if sum(graph[i]) < k - 1:
                return False
        return True
    
    def symmetry_group_order(graph):
        n = len(graph)
        sym_group = set()
        for perm in itertools.permutations(range(n)):
            permuted_graph = [graph[perm.index(i)] for i in range(n)]
            if permuted_graph == graph:
                sym_group.add(tuple(perm))
        return len(sym_group)
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def generate_k_clique_graph(k):
        clique = [[0] * k for _ in range(k)]
        for i in range(k):
            for j in range(i + 1, k):
                clique[i][j] = 1
                clique[j][i] = 1
        graph = [[0] * (k + n - k) for _ in range(k + n - k)]
        for i in range(k):
            for j in range(k):
                graph[i][j] = clique[i][j]
        for i in range(k, k + n - k):
            graph[i][i] = 1
        return graph
    
    n = random.randint(5, 40)
    if random.choice([True, False]):
        graph = generate_random_graph(n)
    else:
        k = min(n, random.randint(2, 10))
        graph = generate_k_clique_graph(k)
    
    instances_tested = 1
    conjecture_holds = True
    counterexample = ""
    
    if is_k_clique(graph, n):
        if symmetry_group_order(graph) < k**2:
            conjecture_holds = False
            counterexample = "k-CLIQUE graph with minimal symmetry group order below Ω(k^2)"
    else:
        if symmetry_group_order(graph) > n**(1/4):
            conjecture_holds = False
            counterexample = "Non-k-CLIQUE graph with minimal symmetry group order above Θ(n^{1/4})"
    
    return {
        "metric_name": "symmetry_group_order",
        "metric_value": symmetry_group_order(graph),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")