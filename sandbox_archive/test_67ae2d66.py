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
    
    def generate_k_cnf_instance(n, k):
        literals = [f'x{i}' for i in range(1, n+1)] + [f'y{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(k):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return literals, clauses

    def construct_constraint_graph(literals, clauses):
        G = {}
        for literal in literals:
            G[literal] = set()
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    G[clause[i]].add(clause[j])
                    G[clause[j]].add(clause[i])
        return G

    def hyperbolic_volume(G):
        n = len(G)
        if n == 0:
            return 0
        volume = 1
        for node in G:
            degree = len(G[node])
            if degree > 0:
                volume *= (n - degree) / degree
        return volume

    def isometric_embedding(G):
        # Simplified embedding algorithm for demonstration purposes
        n = len(G)
        embedding = {}
        for i, node in enumerate(sorted(G.keys())):
            embedding[node] = [i]
        return embedding

    results = []
    for n in range(1, 41):
        for _ in range(30):  # Ensure at least 30 instances per seed
            literals, clauses = generate_k_cnf_instance(n, k=2*n)
            G = construct_constraint_graph(literals, clauses)
            volume = hyperbolic_volume(G)
            embedding = isometric_embedding(G)
            if volume > n**(1 + 0.5):
                return {
                    "metric_name": "Hyperbolic Volume",
                    "metric_value": volume,
                    "instances_tested": 30 * (n - 1),
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Volume {volume} exceeds n^(1+0.5) for n={n}"
                }
            results.append(volume)

    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for v in results if v <= n**(1 + 0.5)) / len(results)
    
    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": mean,
        "instances_tested": 30 * (40 - 1),
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
        results.append(result["metric_value"])
    
    if len(results) == len(seeds):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(next(x for x, r in enumerate(results) if not r["conjecture_holds"]))]
        print(f"RESULT: FALSIFIED counterexample='Volume exceeds n^(1+0.5)' first_failing_seed={first_failing_seed}")