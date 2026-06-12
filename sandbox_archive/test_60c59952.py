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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for k in range(i+1, n):
                factor = matrix[k][i] / matrix[i][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
        
        # Back substitution
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][-1]
            for k in range(i+1, n):
                x[i] -= matrix[i][k] * x[k]
            x[i] /= matrix[i][i]
        
        return x
    
    def random_cnf(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause):
                clauses.append(clause)
        return clauses
    
    def clause_tree_width(clauses: list) -> int:
        n = len(clauses)
        graph = {i: set() for i in range(n)}
        
        for i in range(n):
            for j in range(i+1, n):
                if any(abs(c) == abs(d) for c in clauses[i] for d in clauses[j]):
                    graph[i].add(j)
                    graph[j].add(i)
        
        def dfs(node: int, visited: set) -> int:
            visited.add(node)
            max_width = 0
            neighbors = [n for n in graph[node] if n not in visited]
            while neighbors:
                neighbor = neighbors.pop()
                width = dfs(neighbor, visited)
                max_width = max(max_width, width)
            return max_width + 1
        
        return max(dfs(i, set()) for i in range(n))
    
    def symplectic_volume(clauses: list) -> float:
        n = len(clauses)
        matrix = [[0.0] * (n+1) for _ in range(n+1)]
        
        for i in range(n):
            for j in range(i, n):
                if any(abs(c) == abs(d) for c in clauses[i] for d in clauses[j]):
                    matrix[i][j] = 1.0
                    matrix[j][i] = 1.0
        
        matrix[-1][-1] = 1.0
        for i in range(n):
            matrix[i][-1] = -sum(matrix[i][:i])
        
        return abs(gaussian_elimination(matrix)[-1])
    
    def upper_bound(w: int) -> float:
        # Placeholder function for the upper bound
        return w * math.log2(w)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        clauses = random_cnf(n)
        w_phi = clause_tree_width(clauses)
        volume = symplectic_volume(clauses)
        
        if volume > upper_bound(w_phi):
            conjecture_holds = False
            counterexample = f"n={n}, w(φ)={w_phi}, Volume={volume}"
            break
        
        metric_values.append(volume)
    
    return {
        "metric_name": "Symplectic Volume",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")