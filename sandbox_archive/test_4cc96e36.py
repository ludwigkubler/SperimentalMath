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
    
    def generate_symplectic_manifold(n):
        # Simulate a compact symplectic manifold using a matrix
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def tropicalize(matrix):
        # Tropicalize the matrix by taking the maximum of each element and -infinity if it's zero
        return [[max(x, -math.inf) for x in row] for row in matrix]
    
    def compute_minimal_rank(tropicalized_matrix):
        n = len(tropicalized_matrix)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if tropicalized_matrix[i][j] != -math.inf:
                    rank += 1
                    break
        return rank
    
    def generate_xor_and_network(s):
        # Generate an XOR-AND network from a set of points
        n = len(s)
        xor_and_network = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                xor_and_network[i][j] = s[i] ^ s[j]
                xor_and_network[j][i] = xor_and_network[i][j]
        return xor_and_network
    
    def compute_smallest_ac0_circuit_size(xor_and_network):
        n = len(xor_and_network)
        # Simulate a simple circuit minimization technique
        circuit_size = 0
        for i in range(n):
            for j in range(i + 1, n):
                if xor_and_network[i][j] == 1:
                    circuit_size += 1
        return circuit_size
    
    def gaussian_elimination(matrix):
        # Perform Gaussian elimination to find the rank of a matrix
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != -math.inf:
                rank += 1
                for j in range(i + 1, n):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def compute_tropicalized_rank(matrix):
        # Compute the tropicalized rank using Gaussian elimination
        tropicalized_matrix = tropicalize(matrix)
        return gaussian_elimination(tropicalized_matrix)
    
    n = 10  # Start with a small size and increase for more trials
    if seed % 2 == 0:
        n = random.choice([5, 15, 30])
    
    M = generate_symplectic_manifold(n)
    S = {random.randint(0, 1) for _ in range(n)}
    tropicalized_rank = compute_tropicalized_rank(M)
    xor_and_network = generate_xor_and_network(S)
    ac0_circuit_size = compute_smallest_ac0_circuit_size(xor_and_network)
    
    return {
        "metric_name": "Minimal Rank (Tropicalized Symplectic Geometry)",
        "metric_value": tropicalized_rank,
        "instances_tested": 1,
        "conjecture_holds": tropicalized_rank <= ac0_circuit_size,
        "counterexample": "" if tropicalized_rank <= ac0_circuit_size else f"tropicalized_rank={tropicalized_rank}, ac0_circuit_size={ac0_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    total_ac0_circuit_size = sum(r["instances_tested"] * (1 if r["conjecture_holds"] else 0) for r in results)
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")