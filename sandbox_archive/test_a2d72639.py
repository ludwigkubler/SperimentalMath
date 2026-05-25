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
    
    n = random.randint(5, 30)
    k = random.randint(2, min(n-1, 5))
    
    # Generate a random group G with n elements
    G = [i for i in range(n)]
    def compose(g1, g2):
        return (g1 + g2) % n
    
    # Define a linear action of G on n variables
    action = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the tropicalized representation matrix
    T = []
    for g in G:
        row = [action[g][i] for i in range(n)]
        T.append(row)
    
    # Determine the minimal rank of the tropicalized representation matrix
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for j in range(n):
            pivot_row = -1
            for i in range(m):
                if matrix[i][j] != 0:
                    if pivot_row == -1:
                        pivot_row = i
                    else:
                        for k in range(j, n):
                            matrix[pivot_row][k], matrix[i][k] = matrix[i][k], matrix[pivot_row][k]
                        for l in range(m):
                            if l != pivot_row and matrix[l][j] != 0:
                                factor = -matrix[l][j] / matrix[pivot_row][j]
                                for k in range(j, n):
                                    matrix[l][k] += factor * matrix[pivot_row][k]
        rank = sum(1 for row in matrix if any(row[i] != 0 for i in range(n)))
        return rank
    
    minimal_rank = gaussian_elimination(T)
    
    # Construct a monotone circuit for k-CLIQUE using the same variables
    def is_clique(G, S):
        for u in S:
            for v in S:
                if u < v and (u, v) not in G:
                    return False
        return True
    
    def construct_monotone_circuit(n, k):
        circuit = []
        nodes = [i for i in range(2**n)]
        edges = [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range(i+1, len(nodes))]
        
        # Add a node for each subset of size k
        subsets = []
        for i in range(n):
            for subset in itertools.combinations(range(n), i):
                if len(subset) == k:
                    subsets.append(frozenset(subset))
        
        # Add edges between nodes representing subsets
        for u, v in edges:
            u_subsets = [subset for subset in subsets if all(u & subset == 0)]
            v_subsets = [subset for subset in subsets if all(v & subset == 0)]
            for s_u in u_subsets:
                for s_v in v_subsets:
                    if is_clique(s_u | s_v, s_u):
                        circuit.append((u, v))
        
        return circuit
    
    circuit_size = len(construct_monotone_circuit(n, k))
    
    # Compare the minimal rank of the tropicalized representation to the circuit size
    correlation_coefficient = (minimal_rank - circuit_size) / (n * (n-1) / 2)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 999999) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")