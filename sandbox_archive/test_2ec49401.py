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
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def clique_complex(edges):
        cliques = set()
        n = len(edges)
        for subset_size in range(2, n + 1):
            for subset in itertools.combinations(range(n), subset_size):
                is_clique = True
                for u, v in itertools.combinations(subset, 2):
                    if (u, v) not in edges and (v, u) not in edges:
                        is_clique = False
                        break
                if is_clique:
                    cliques.add(tuple(sorted(subset)))
        return cliques
    
    def euler_characteristic(cliques):
        return sum((-1)**(len(c) - 1) * len(list(itertools.combinations(c, k))) for c in cliques for k in range(len(c) + 1))
    
    def tseitin_resolution_length(edges):
        n = len(edges)
        clauses = []
        for u, v in edges:
            clauses.append([u, -v])
            clauses.append([-u, v])
        for i in range(n):
            clauses.append([i] + [-j for j in range(n) if (i, j) not in edges and (-i, j) not in edges])
        resolution_length = 0
        while True:
            new_clauses = []
            added_clause = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if new_clause not in clauses:
                            new_clauses.append(new_clause)
                            added_clause = True
            if not added_clause:
                break
            clauses.extend(new_clauses)
            resolution_length += len(new_clauses)
        return resolution_length
    
    n = random.randint(5, 40)
    edges = generate_random_graph(n)
    cliques = clique_complex(edges)
    chi_G = euler_characteristic(cliques)
    res_len = tseitin_resolution_length(edges)
    
    c = 1 / math.log2(n)  # Example constant
    if res_len >= 2**(c * chi_G):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Graph with n={n}, A={edges}"
    
    return {
        "metric_name": "Tseitin Resolution Length",
        "metric_value": res_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")