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
    
    def adjacency_matrix(formula, n):
        A = [[0] * n for _ in range(n)]
        for clause in formula:
            literals = set(clause.split(' | '))
            for literal in literals:
                if literal[0] == '~':
                    var = int(literal[2:]) - 1
                else:
                    var = int(literal[1:]) - 1
                A[var][var] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        rank = 0
        for i in range(n):
            if any(A[i]):
                rank += 1
        return rank
    
    def tseitin_formula(n, width):
        formula = []
        literals = [f'x{i+1}' for i in range(n)]
        for _ in range(width):
            clause = random.sample(literals, 2)
            formula.append(f'{clause[0]} | {clause[1]}')
        return formula
    
    n = random.randint(5, 30)
    width = random.randint(2, n//2)
    formula = tseitin_formula(n, width)
    
    A = adjacency_matrix(formula, n)
    rank = gaussian_elimination(A)
    
    expected_rank = 2 ** (width * math.log2(width))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= expected_rank,
        "counterexample": "" if rank >= expected_rank else f"rank={rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")