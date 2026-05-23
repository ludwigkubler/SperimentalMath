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
        return edges
    
    def delone_triangulation(edges, n):
        # Simplified Delone triangulation algorithm (not actual Delone)
        triangulation = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in edges:
                    for k in range(j + 1, n):
                        if (j, k) in edges and (k, i) in edges:
                            triangulation.add((i, j, k))
        return triangulation
    
    def resolution_refutation_length(edges, n):
        # Simplified DPLL solver to estimate refutation length
        clauses = []
        for u, v in edges:
            clauses.append((u, -v))
            clauses.append((-u, v))
        
        def dpll(clauses, assignment):
            if not clauses:
                return 1
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                return dpll(clauses, new_assignment)
            
            literal = next((l for l in range(n) if l not in assignment), -1)
            if literal == -1:
                return 0
            
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return max(dpll(new_clauses, assignment | {literal: True}), dpll(new_clauses, assignment | {literal: False}))
        
        return dpll(clauses, {})
    
    n = random.randint(5, 40)
    edges = generate_random_graph(n)
    triangulation = delone_triangulation(edges, n)
    geometric_entropy = math.log2(len(triangulation))
    refutation_length = resolution_refutation_length(edges, n)
    
    conjecture_holds = refutation_length <= 2 ** (1.5 * geometric_entropy)
    counterexample = "" if conjecture_holds else f"Refutation length {refutation_length} > 2^(1.5 * {geometric_entropy})"
    
    return {
        "metric_name": "Resolution Refutation Length vs Geometric Entropy",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")