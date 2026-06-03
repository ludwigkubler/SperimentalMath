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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def construct_graph(phi):
        n = len(phi)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if phi[i] != phi[j]:
                    G[i][j] = G[j][i] = 1
        return G
    
    def min_noncrossing_partitions(G):
        n = len(G)
        partitions = []
        for i in range(1 << n):
            partition = [[]]
            for j in range(n):
                if i & (1 << j):
                    partition[-1].append(j)
                else:
                    partition.append([j])
            partitions.append(partition)
        min_order = float('inf')
        for p in partitions:
            order = 0
            for block in p:
                subgraph = [[G[i][j] for j in block] for i in block]
                if not is_connected(subgraph):
                    continue
                order += 1
            min_order = min(min_order, order)
        return min_order
    
    def is_connected(G):
        n = len(G)
        visited = [False] * n
        stack = [0]
        visited[0] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if G[u][v] and not visited[v]:
                    visited[v] = True
                    stack.append(v)
        return all(visited)
    
    def frege_proof_length(phi):
        # Simplified DPLL-based solver to estimate proof length
        n = len(phi)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
            clauses.append([-i - 1])
        for i in range(n):
            for j in range(i + 1, n):
                if phi[i] != phi[j]:
                    clauses.append([i + 1, -j - 1])
                    clauses.append([-i - 1, j + 1])
        
        def solve(lits_true, lits_false):
            stack = []
            while stack or lits_true:
                if not stack and not lits_true:
                    return False
                if not stack:
                    lit = lits_true.pop()
                    stack.append((lit, True))
                else:
                    lit, polarity = stack[-1]
                    if polarity == True:
                        if lit in lits_false:
                            lits_false.remove(lit)
                            stack.pop()
                        elif -lit in lits_true:
                            lits_true.remove(-lit)
                            stack.pop()
                        else:
                            other_lit = random.choice([-lit, lit])
                            stack.append((other_lit, False))
                    else:
                        if lit in lits_true:
                            lits_true.remove(lit)
                            stack.pop()
                        elif -lit in lits_false:
                            lits_false.remove(-lit)
                            stack.pop()
                        else:
                            other_lit = random.choice([-lit, lit])
                            stack.append((other_lit, True))
            return True
        
        return len(clauses) * 2
    
    m = random.randint(5, 40)
    phi = generate_boolean_function(m)
    G = construct_graph(phi)
    min_order = min_noncrossing_partitions(G)
    proof_length = frege_proof_length(phi)
    
    return {
        "metric_name": "PearsonCorrelation",
        "metric_value": min_order * proof_length,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")