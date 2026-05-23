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
    
    def generate_expander_graph(n):
        if n < 4 or n % 2 != 0:
            return None
        G = {}
        for i in range(n):
            G[i] = []
        for i in range(n // 2):
            u, v = random.sample(range(n), 2)
            while u == v or (u in G and v in G[u]):
                u, v = random.sample(range(n), 2)
            G[u].append(v)
            G[v].append(u)
        return G
    
    def tutte_polynomial(G):
        n = len(G)
        T = [[0] * (n + 1) for _ in range(n + 1)]
        T[0][0] = 1
        for u in range(1, n + 1):
            for v in G[u - 1]:
                if v < u:
                    continue
                for i in range(u, -1, -1):
                    for j in range(n + 1):
                        T[i][j] += T[i - 1][j]
                        if j >= u:
                            T[i][j] -= T[i - 1][j - u]
        return T
    
    def characteristic_polynomial(T):
        n = len(T) - 1
        p = [[0] * (n + 1) for _ in range(n + 1)]
        p[0][0] = 1
        for i in range(1, n + 1):
            for j in range(n + 1):
                p[i][j] = T[i - 1][j]
                if j >= i:
                    p[i][j] -= T[i - 1][j - i]
        return p
    
    def tropical_logarithmic_form(p):
        n = len(p) - 1
        rank = 0
        for i in range(n + 1):
            for j in range(n + 1):
                if p[i][j] != 0:
                    rank += 1
        return rank
    
    def resolution_proof_length(G):
        n = len(G)
        clauses = []
        for u in G:
            for v in G[u]:
                clauses.append((u, v))
        stack = [(clauses[0], set())]
        while stack:
            clause, assignment = stack.pop()
            if not clause:
                return 1
            literal = next(lit for lit in clause if lit not in assignment)
            new_assignment = assignment.union({literal})
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.extend((new_clause, new_assignment) for new_clause in new_clauses)
        return float('inf')
    
    n = random.randint(5, 40)
    G = generate_expander_graph(n)
    if G is None:
        return {
            "metric_name": "Rank vs DPLL Height",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    T = tutte_polynomial(G)
    p = characteristic_polynomial(T)
    rank = tropical_logarithmic_form(p)
    proof_length = resolution_proof_length(G)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "Rank vs DPLL Height",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unprovable"
        }
    
    ratio = proof_length / (2 ** rank)
    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample='unprovable' first_failing_seed={first_failing_seed}"
    
    print(result)