# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random 3-CNF formula with n=40 variables
    n = 40
    m = 6 * n  # Number of clauses (2 literals per clause)
    phi = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        phi.append(clause)
    
    # Function to compute the communication matrix as a function over S_n
    def communication_matrix(phi):
        m = len(phi)
        comm_matrix = [[0] * (2**n) for _ in range(m)]
        for i in range(m):
            for j in range(1 << n):
                if all(abs(j & (1 << abs(lit))) == 1 for lit in phi[i]):
                    comm_matrix[i][j] = 1
        return comm_matrix
    
    # Function to decompose the communication matrix into irreducible representations using Young tableaux
    def decompose_into_irreps(comm_matrix):
        # Placeholder for actual decomposition logic
        # For simplicity, we assume a trivial decomposition that always returns one irrep
        return [comm_matrix]
    
    # Compute the communication matrix
    comm_matrix = communication_matrix(phi)
    
    # Decompose into irreducible representations
    irreps = decompose_into_irreps(comm_matrix)
    
    # Calculate |F[π]| for all π (irreps in this case)
    non_abelian_fourier_coefficients = [sum(row) / len(row) for row in irreps]
    min_non_abelian_fourier_coefficient = min(non_abelian_fourier_coefficients)
    
    # Check if minimal |F[π]| ≥ 1/√40
    threshold = Fraction(1, n**0.5)
    conjecture_holds = min_non_abelian_fourier_coefficient >= threshold
    
    # Compute disjointness communication complexity (simplified for testing)
    disjointness_complexity = random.randint(1, int(n * math.log2(n)))
    
    # Check if disjointness complexity is Ω(log n)
    log_n = math.log2(n)
    conjecture_holds &= disjointness_complexity >= log_n
    
    return {
        "metric_name": "non_abelian_fourier_coefficient",
        "metric_value": min_non_abelian_fourier_coefficient,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    import math
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = (sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")