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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def monomial_ideal(edges):
        ideal = set()
        for edge in edges:
            x, y = sorted(edge)
            ideal.add(f"x{x+1}*y{y+1}")
        return ideal
    
    def kronecker_dimension(ideal):
        n = len(ideal)
        if n == 0:
            return 0
        matrix = []
        for monomial in ideal:
            row = [0] * (n + 1)
            for term in monomial.split('*'):
                var, exp = term[0], int(term[1:])
                if var == 'x':
                    row[exp - 1] += 1
                else:
                    row[-1] -= exp
            matrix.append(row)
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if matrix[j][i] != 0), None)
            if pivot is not None:
                rank += 1
                for j in range(n + 1):
                    matrix[i][j], matrix[pivot][j] = matrix[pivot][j], matrix[i][j]
                for j in range(n):
                    if i != j:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n + 1):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def minimal_rank(edges):
        n = len(edges)
        graph = [set() for _ in range(n)]
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        
        visited = set()
        rank = 0
        
        def dfs(node):
            nonlocal rank
            if node not in visited:
                visited.add(node)
                rank += 1
                for neighbor in graph[node]:
                    dfs(neighbor)
        
        for i in range(n):
            if i not in visited:
                dfs(i)
        
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = generate_random_graph(n)
    ideal = monomial_ideal(edges)
    kronecker_dim = kronecker_dimension(ideal)
    min_rank = minimal_rank(edges)
    
    if min_rank == 0:
        return {
            "metric_name": "Kronecker Dimension",
            "metric_value": kronecker_dim,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_rank_is_zero"
        }
    
    c = Fraction(1, n)
    if kronecker_dim <= c * min_rank:
        return {
            "metric_name": "Kronecker Dimension",
            "metric_value": kronecker_dim,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Kronecker Dimension",
            "metric_value": kronecker_dim,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"kronecker_dim={kronecker_dim}, c*min_rank={c * min_rank}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")