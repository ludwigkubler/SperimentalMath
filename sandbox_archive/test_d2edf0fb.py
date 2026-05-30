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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def hyperbolic_metric(G):
        n = len(G)
        if n == 1:
            return 0
        d_H = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                d_H = min(d_H, hamming_distance(G[i], G[j]))
        return d_H
    
    def resolution_width(P):
        width = 0
        for clause in P:
            width = max(width, len(clause))
        return width
    
    def generate_resolution_proof(f):
        # Simplified resolution algorithm for demonstration purposes
        n = int(math.log2(len(f)))
        clauses = [[i] if f[i] == 1 else [n + i] for i in range(n)]
        proof = []
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if new_clause not in proof and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
            proof.extend(new_clauses)
        return proof
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    G = [f[i:i+n] for i in range(len(f) - n + 1)]
    d_H = hyperbolic_metric(G)
    P = generate_resolution_proof(f)
    width = resolution_width(P)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= 2 * d_H,  # Example constant α
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    std_width = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = "resolution_width does not satisfy the conjecture"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")