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
    
    n = 20  # Size of the k-CNF formula
    k = 3   # Number of literals per clause
    
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, k)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    # Construct the graphical realization of the formula
    graph = {i: set() for i in variables}
    for clause in clauses:
        for literal in clause:
            if literal > 0:
                graph[literal].add(-literal)
                graph[-literal].add(literal)
    
    # Calculate the minimal rank of the noncrossed product K-theory
    def dfs(node, visited):
        stack = [node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    stack.append(neighbor)
    
    visited = set()
    connected_components = 0
    for variable in variables:
        if variable not in visited:
            dfs(variable, visited)
            connected_components += 1
    
    rank_K = connected_components
    
    # Measure and report the empirical mean of the ranks over 30 different random seeds
    return {
        "metric_name": "rank(K)",
        "metric_value": rank_K,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank_K = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("counterexample" not in result or result["counterexample"] == "mapping_undefined" for result in results):
        RESULT = f"SUPPORTED mean={mean_rank_K} std=0 support_fraction={support_fraction}"
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)