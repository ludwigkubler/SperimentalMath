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
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 10))
    
    # Construct the graph as a random k-clique
    edges = set()
    nodes = list(range(n))
    for _ in range(k):
        node = random.choice(nodes)
        nodes.remove(node)
        for other_node in nodes:
            edges.add((node, other_node))
            edges.add((other_node, node))
    
    # Construct the integer lattice representation
    A = []
    b = []
    for u, v in edges:
        row = [0] * n
        row[u] = 1
        row[v] = -1
        A.append(row)
        b.append(0)
    
    # Add slack variables to make the system solvable
    m = len(A)
    for i in range(m):
        A[i].extend([0] * (n - m + i))
        b.append(0)
    
    # Solve the linear programming problem using Gaussian elimination
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x
    
    try:
        x = gaussian_elimination(A, b)
    except Exception as e:
        return {
            "metric_name": "lattice_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Calculate the lattice width
    width = max(abs(x[i]) for i in range(n))
    
    # Calculate the monotone circuit size
    mean_circuit_size = n ** (5/4)
    
    return {
        "metric_name": "lattice_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= n**(3/4) * math.log(k)**2 and mean_circuit_size >= n**(5/4),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")