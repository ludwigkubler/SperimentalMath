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
    
    def generate_tseitin_formula(n):
        if n <= 1:
            return []
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(2, n+1):
            clauses.append([f'-{variables[0]}', f'{variables[i-1]}'])
        return clauses
    
    def is_expander_graph(G, n):
        degree = sum(len(neighbors) for neighbors in G.values()) / (2 * n)
        return degree >= 3
    
    def generate_quandle_representation(V):
        quandles = {}
        for v in V:
            quandles[v] = random.choice(list(quandles.keys()) + [v])
        return quandles
    
    def compute_rank(Q, V):
        rank = len(set(Q.values()))
        return rank
    
    def dpll(clauses, assignment, Q, V):
        if not clauses:
            return True
        clause = next(c for c in clauses if any(v not in assignment or (assignment[v] == 'T' and v in Q and Q[v] != c[0]) for v in c))
        literal = next(l for l in clause if l not in assignment)
        assignment[literal] = 'T'
        if dpll(clauses, assignment, Q, V):
            return True
        del assignment[literal]
        assignment[literal] = 'F'
        if dpll(clauses, assignment, Q, V):
            return True
        del assignment[literal]
        return False
    
    def compute_resolution_proof_length(clauses):
        assignment = {}
        proof_length = 0
        while not dpll(clauses, assignment, {}, range(len(clauses))):
            proof_length += 1
        return proof_length
    
    n = random.randint(5, 40)
    G = {i: [] for i in range(n)}
    for _ in range(int(n * (n - 1) / 2)):
        u, v = random.sample(range(n), 2)
        G[u].append(v)
        G[v].append(u)
    
    if not is_expander_graph(G, n):
        return {
            "metric_name": "Rank vs DPLL Length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not an expander"
        }
    
    F = generate_tseitin_formula(n)
    Q = generate_quandle_representation(list(G.keys()))
    rank_Q = compute_rank(Q, list(G.keys()))
    proof_length = compute_resolution_proof_length(F)
    
    return {
        "metric_name": "Rank vs DPLL Length",
        "metric_value": rank_Q / (proof_length + 1) if proof_length > 0 else None,
        "instances_tested": 1,
        "conjecture_holds": rank_Q >= math.exp(proof_length),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "unknown"
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"seed={r['seed']}, rank_Q={r['metric_value']}, proof_length={1 / (r['metric_value'] + 1)}"
                break
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)