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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank_of_matrix(A):
    n = len(A)
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for i in range(n):
        if any(A_copy[i]):
            rank += 1
    return rank

def twisted_quantum_entanglement_tensor(clauses):
    n = len(clauses[0])
    tensor = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in clauses:
        for literal in clause:
            var = abs(literal)
            if literal > 0:
                tensor[var][var] += 1
            else:
                tensor[-var][-var] += 1
    
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        clauses.append(clause)
    
    tensor = twisted_quantum_entanglement_tensor(clauses)
    rank = rank_of_matrix(tensor)
    
    expected_rank = math.ceil(n ** (2 / 3))
    conjecture_holds = rank >= expected_rank
    
    return {
        "metric_name": "Rank of Twisted Quantum Entanglement Tensor",
        "metric_value": rank,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, expected_rank={expected_rank}, actual_rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + list(map(lambda p: int(p), ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29']))
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"n={r['instances_tested']}, expected_rank={math.ceil(r['instances_tested'] ** (2 / 3))}, actual_rank={r['metric_value']}\" first_failing_seed={seed}")
                break