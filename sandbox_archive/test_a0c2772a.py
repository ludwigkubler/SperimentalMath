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
        if n < 2:
            return []
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
            for j in range(i + 1, n):
                clauses.append([-variables[i], -variables[j]])
                clauses.append([variables[i], variables[j]])
        return clauses
    
    def is_expander_graph(G, epsilon=0.5):
        n = len(G)
        degrees = [sum(1 for v in G if (u, v) in G or (v, u) in G) for u in range(n)]
        avg_degree = sum(degrees) / n
        return all(d >= avg_degree * epsilon for d in degrees)
    
    def compute_quandle_representation(V):
        quandles = {}
        for v in V:
            quandles[v] = {v}
        return quandles
    
    def resolution_proof_length(F, quandles):
        # Simplified DPLL solver to estimate proof length
        stack = []
        while F:
            clause = next((c for c in F if len(c) == 1), None)
            if not clause:
                return -1
            literal = clause[0]
            F.remove(clause)
            for c in F:
                if literal in c:
                    c.remove(literal)
                    if not c:
                        F.remove(c)
                elif -literal in c:
                    c.remove(-literal)
                    if not c:
                        F.remove(c)
        return len(stack)
    
    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    while not is_expander_graph(G):
        edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
        random.shuffle(edges)
        for (u, v) in edges[:n - 1]:
            G[u].add(v)
            G[v].add(u)
    
    F = generate_tseitin_formula(n)
    quandles = compute_quandle_representation(list(G))
    rank_Q = sum(len(q) for q in quandles.values())
    proof_length = resolution_proof_length(F, quandles)
    
    if proof_length == -1:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL solver failed to find a refutation"
        }
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank_Q / proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank_Q >= 2 ** math.floor(proof_length / 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Rank vs DPLL Heig"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")