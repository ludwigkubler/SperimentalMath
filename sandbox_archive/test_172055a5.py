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
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for clause in formula.split(' & '):
            if '|' in clause:
                literals = clause.split(' | ')
                for literal in literals:
                    var = literal.strip('~')
                    idx = int(var[1:]) - 1
                    matrix[idx][idx] = 1
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(n):
            if augmented_matrix[i][i] == 0:
                for j in range(i+1, n):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    return i
            pivot = augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i and augmented_matrix[j][i] != 0:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return n
    
    def geometric_quantization_rank(matrix):
        # Simplified rank calculation
        return rank(matrix)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    w_G = width(formula)
    A = adjacency_matrix(formula, n)
    phi_A = geometric_quantization_rank(A)
    expected = 2 ** (math.ceil(math.log(w_G, 2)))
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": phi_A,
        "instances_tested": 1,
        "conjecture_holds": phi_A >= expected,
        "counterexample": "" if phi_A >= expected else f"rank={phi_A}, expected={expected}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")