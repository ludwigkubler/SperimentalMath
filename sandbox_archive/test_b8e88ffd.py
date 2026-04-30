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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(cols):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]

def is_idempotent(matrix):
    return gaussian_elimination(matrix) == 0

def count_monomials(idempotents):
    return sum(1 for idempotent in idempotents if is_idempotent(idempotent))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    instances_tested = 30
    total_monomial_count = 0
    
    for _ in range(instances_tested):
        # Generate a random 2-CNF formula with n variables
        clauses = []
        for _ in range(n * (n - 1) // 2):
            literals = [random.choice([f'x{i+1}', f'x{i+1}']) for i in range(n)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        
        # Construct the communication matrix
        comm_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if random.choice([True, False]):
                    comm_matrix[i][j] = 1
                    comm_matrix[j][i] = 1
        
        # Decompose into idempotents (simplified version)
        idempotents = [comm_matrix]
        
        monomial_count = count_monomials(idempotents)
        total_monomial_count += monomial_count
    
    mean_monomial_count = total_monomial_count / instances_tested
    conjecture_holds = abs(mean_monomial_count - 2**(n/2)) < 1e-6
    counterexample = "monomial_count_deviation" if not conjecture_holds else ""
    
    return {
        "metric_name": "monomial_count",
        "metric_value": mean_monomial_count,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [727, 773, 821, 877, 929]  # Default to a list of primes if no seeds are provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_monomial_count = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_monomial_count} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_monomial_count} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")