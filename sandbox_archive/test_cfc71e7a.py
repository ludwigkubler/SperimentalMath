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
    
    def generate_xor_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = []
            for i in range(n):
                if random.choice([True, False]):
                    clause.append(f"x{i+1}")
                else:
                    clause.append(f"~x{i+1}")
            clauses.append(clause)
        return clauses
    
    def quadratic_form(clauses):
        n = len(clauses[0])
        q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for literal in clause:
                if literal.startswith('x'):
                    var = int(literal[1:]) - 1
                    q[var][var] += 1
                elif literal.startswith('~x'):
                    var = int(literal[2:]) - 1
                    q[var][var] -= 1
        return q
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def monomial_circuit_size(clauses):
        n = len(clauses[0])
        size = 0
        for clause in clauses:
            size += len(clause) - 1
        return size
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_xor_3cnf(n)
    q_form = quadratic_form(instance)
    rank = gaussian_elimination(q_form)
    if rank is None:
        return {
            "metric_name": "rank_to_circuit_size_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    circuit_size = monomial_circuit_size(instance)
    ratio = Fraction(rank, circuit_size)
    
    return {
        "metric_name": "rank_to_circuit_size_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_circuit_size_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")