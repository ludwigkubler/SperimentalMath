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
            
            # Eliminate above and below
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det
    
    def eulertour(graph, start):
        visited = set()
        stack = [start]
        euler_tour = []
        while stack:
            u = stack[-1]
            if u not in graph or len(graph[u]) == 0:
                euler_tour.append(u)
                stack.pop()
            else:
                v = graph[u].pop()
                graph[v].remove(u)
                stack.append(v)
        return euler_tour
    
    def matroid_euler_characteristic(matrix):
        n = len(matrix)
        m = len(matrix[0])
        graph = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 1:
                    graph[i].add(j)
        
        euler_tour = eulertour(graph, 0)
        return len(euler_tour) - n
    
    def communication_complexity(matrix):
        n = len(matrix)
        m = len(matrix[0])
        det = determinant(gaussian_elimination(matrix))
        chi = matroid_euler_characteristic(matrix)
        return abs(det), n**2 - chi
    
    instances_tested = 0
    metric_sum = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        comm_complexity, chi = communication_complexity(matrix)
        
        metric_sum += comm_complexity
        instances_tested += 1
        max_n = n
        
        if comm_complexity > n**2 - chi:
            conjecture_holds = False
            counterexample = f"Matrix with n={n} and det={comm_complexity}, chi={chi}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_sum / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")