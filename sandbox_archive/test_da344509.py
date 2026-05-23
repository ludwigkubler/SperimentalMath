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
    
    def generate_bp(n):
        # Generate a random read-twice branching program for IP_2 with size n
        bp = []
        for _ in range(n):
            if random.choice([True, False]):
                bp.append(random.randint(0, 1))
            else:
                bp.append((random.randint(0, 1), random.randint(0, 1)))
        return bp
    
    def ip2_function(bp):
        # Evaluate the IP_2 function for a given read-twice branching program
        result = 0
        for bit in bp:
            if isinstance(bit, tuple):
                result += bit[0] * bit[1]
            else:
                result += bit
        return result
    
    def coxeter_group(bp):
        # Generate the Coxeter group associated with a read-twice branching program
        n = len(bp)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            if isinstance(bp[i], tuple):
                G[i][i] = 1
                G[i][(i + 1) % n] = 2
                G[(i + 1) % n][i] = 2
            else:
                G[i][i] = 1
        return G
    
    def coxeter_matrix_invariant(G):
        # Compute the Coxeter matrix invariant of a Coxeter group
        n = len(G)
        det = determinant(G, n)
        if det == 0:
            return float('inf')
        return abs(det) ** (1 / n)
    
    def determinant(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix, n - 1)
        return det
    
    def log_size(bp):
        # Compute the logarithm of the size of a read-twice branching program
        return math.log(len(bp))
    
    def is_trivial_bp(bp):
        # Check if a read-twice branching program computes the trivial IP_2 function
        return all(isinstance(bit, int) for bit in bp)
    
    n = random.randint(5, 40)
    bp = generate_bp(n)
    G = coxeter_group(bp)
    rho_G = coxeter_matrix_invariant(G)
    log_p = log_size(bp)
    
    if is_trivial_bp(bp):
        conjecture_holds = rho_G >= n
    else:
        conjecture_holds = rho_G <= 10 * log_p
    
    return {
        "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
        "metric_value": rho_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Trivial IP_2 function"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 10 * math.log(len(bp)) for bp, r in zip(results)):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] > 10 * math.log(len(bp)))
        print(f"RESULT: FALSIFIED counterexample=\"Trivial IP_2 function\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")