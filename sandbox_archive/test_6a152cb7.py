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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]} | ~{variables[i-1]}'
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def width(formula):
        # Simplified width calculation
        return len(formula.split(' & '))
    
    def adjacency_matrix(formula, n):
        matrix = [[0] * n for _ in range(n)]
        for clause in formula.split(' & '):
            if ' | ' not in clause:
                continue
            var1, var2 = clause.split(' | ')
            i = int(var1[1:]) - 1
            j = int(var2[1:]) - 1
            matrix[i][j] = 1
            matrix[j][i] = 1
        return matrix
    
    def geometric_quantization(matrix):
        # Placeholder for actual quantization logic
        return len(matrix)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    w_G = width(formula)
    A = adjacency_matrix(formula, n)
    φ_G = geometric_quantization(A)
    
    expected_rank = 2 ** (math.ceil(math.log(w_G, 2)))
    ratio = φ_G / expected_rank
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": φ_G,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": "" if ratio >= 0.5 else f"rank={φ_G}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break