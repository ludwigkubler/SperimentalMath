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
    
    def generate_random_graph(n):
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        return G
    
    def cocomplex_rank(G):
        n = len(G)
        A = [row[:] for row in G]
        rank = 0
        for i in range(n):
            if sum(A[i]) == 0:
                continue
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[pivot_row], A[i] = A[i], A[pivot_row]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def tseitin_formula(G):
        n = len(G)
        variables = set()
        clauses = []
        
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 0:
                    continue
                clause = [f"x{i}{j}"]
                for k in range(n):
                    if k != i and k != j:
                        clause.append(f"~x{k}{i}")
                        clause.append(f"~x{k}{j}")
                        variables.add(k)
                clauses.append(clause)
        
        return clauses
    
    n = 20
    G = generate_random_graph(n)
    rank = cocomplex_rank(G)
    tseitin_clauses = tseitin_formula(G)
    
    if not tseitin_clauses:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    resolution_proof_length = len(tseitin_clauses)
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": resolution_proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank >= math.log(n, 2) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")