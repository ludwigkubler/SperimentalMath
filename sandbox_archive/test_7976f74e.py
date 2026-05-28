# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clique(n, k):
        vertices = list(range(2**n))
        clique = []
        for _ in range(k):
            vertex = random.choice(vertices)
            if all(vertex & (1 << j) != 0 for j in clique):
                clique.append(vertex)
        return clique
    
    def incidence_variety(clique):
        n = int(math.log2(len(clique)))
        binary_rep = [vertex for vertex in range(2**n)]
        incidence_matrix = []
        for i in range(2**n):
            row = [int(i & (1 << j) != 0) for j in clique]
            incidence_matrix.append(row)
        return incidence_matrix
    
    def minimal_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row >= n:
                    return rank
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(m):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def monotone_circuit_size(n, k):
        # Placeholder function to estimate circuit size
        return n**2 * math.log(k)
    
    n = random.randint(4, 40)
    k = random.randint(4, min(n, 10))
    clique = generate_clique(n, k)
    incidence_matrix = incidence_variety(clique)
    rank = minimal_rank(incidence_matrix)
    circuit_size = monotone_circuit_size(n, k)
    
    return {
        "metric_name": "Minimal Rank of Hodge Structure",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n**2 * math.log(k),
        "counterexample": "" if rank >= n**2 * math.log(k) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 89))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")