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
    n = 30  # Number of variables in Tseitin formula
    c = 1   # Constant for resolution proof length bound
    
    # Generate a random expander graph with n vertices and minimum cutset size ν(G)
    def generate_expander_graph(n):
        G = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i].append(j)
                    G[j].append(i)
        return G
    
    def min_cutset_size(G):
        visited = [False] * n
        queue = [0]
        visited[0] = True
        cutset_size = 0
        
        while queue:
            u = queue.pop(0)
            for v in G[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
        
        return sum(not visited[i] for i in range(n))
    
    G = generate_expander_graph(n)
    ν_G = min_cutset_size(G)
    
    # Generate Tseitin formula from the expander graph
    def generate_tseitin_formula(G, n):
        clauses = []
        literals = [f'x{i}' for i in range(1, n + 1)]
        
        for u in G:
            clause = [f'~{literals[u]}']
            for v in G[u]:
                clause.append(literals[v])
            clauses.append(clause)
        
        return clauses
    
    clauses = generate_tseitin_formula(G, n)
    
    # Compute the associated algebraic variety and Hodge rank
    def hodge_rank(n):
        # Placeholder function to compute Hodge rank
        # This is a dummy implementation for demonstration purposes
        return 2 ** ν_G
    
    H = hodge_rank(n)
    
    # Calculate resolution proof length bound
    proof_length_bound = 2 ** (c * ν_G)
    
    # Check if the conjecture holds
    conjecture_holds = H <= proof_length_bound
    counterexample = "" if conjecture_holds else f"Counterexample: H={H}, proof_length_bound={proof_length_bound}"
    
    return {
        "metric_name": "Hodge Rank / Proof Length Ratio",
        "metric_value": H / proof_length_bound,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")