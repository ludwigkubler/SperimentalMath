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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            A[i] = [x * factor for x in A[i]]
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = graph[j][i] = 1
        return graph

    def fundamental_group_generators(G):
        n = len(G)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if G[i][j]]
        generators = []
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if G[node][neighbor] and not visited[neighbor]:
                        stack.append(neighbor)
                        generators.append((node, neighbor))
        return len(generators)

    def dpll(Tseitin_formula):
        def solve(formula, assignment):
            if not formula:
                return True
            literal = next(l for l in formula if isinstance(l, int) or l[0] != '¬')
            pos_var = abs(literal)
            neg_var = -pos_var
            if pos_var in assignment and assignment[pos_var]:
                return solve(formula, assignment)
            elif neg_var in assignment and not assignment[neg_var]:
                return solve(formula, assignment)
            else:
                assignment[pos_var] = True
                if solve(formula, assignment):
                    return True
                assignment[pos_var] = False
                assignment[neg_var] = True
                if solve(formula, assignment):
                    return True
                assignment[neg_var] = False
                return False
        
        n = len(Tseitin_formula)
        assignment = {}
        return solve(Tseitin_formula, assignment)

    def tseitin_formula(G):
        n = len(G)
        Tseitin_formula = []
        for i in range(n):
            Tseitin_formula.append((i + 1,))
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    Tseitin_formula.append(('¬', i + 1, '¬', j + 1))
                    Tseitin_formula.append((i + 1, j + 1))
        return Tseitin_formula

    def simulate_dpll(G):
        Tseitin = tseitin_formula(G)
        depth = 0
        stack = [Tseitin]
        while stack:
            formula = stack.pop()
            if not formula:
                break
            literal = next(l for l in formula if isinstance(l, int) or l[0] != '¬')
            pos_var = abs(literal)
            neg_var = -pos_var
            if pos_var in assignment and assignment[pos_var]:
                continue
            elif neg_var in assignment and not assignment[neg_var]:
                continue
            else:
                assignment[pos_var] = True
                stack.append(formula)
                depth += 1
        return depth

    n = random.randint(5, 40)
    G = generate_random_graph(n)
    μ_G = fundamental_group_generators(G)
    Tseitin = tseitin_formula(G)
    depth = simulate_dpll(G)

    conjecture_holds = depth >= 2 ** (0.1 * μ_G)
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices and μ(G)={μ_G}, DPLL depth={depth}"
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")