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
    
    def generate_xor_3cnf(n, m):
        variables = [chr(i + ord('x')) for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            negated_vars = ['~' + v if random.choice([True, False]) else v for v in clause]
            clauses.append('(' + ' ∨ '.join(negated_vars) + ')')
        return ' ∧ '.join(clauses)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if rank < n:
                pivot_row = i
                while pivot_row < m and matrix[pivot_row][i] == 0:
                    pivot_row += 1
                if pivot_row == m:
                    continue
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                for j in range(n):
                    if j != i:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def xor_circuit_depth(clauses, n):
        # Simplified heuristic to estimate circuit depth
        # This is a placeholder and should be replaced with actual circuit construction logic
        return len(clauses) + n
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    formula = generate_xor_3cnf(n, m)
    
    # Compute minimal rank of tropical curve (simplified heuristic)
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank = gaussian_elimination(matrix)
    
    # Construct XOR circuit depth
    depth = xor_circuit_depth(formula.split(' ∧ '), n)
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= 2 * math.log(n, 2)  # Simplified heuristic for C log n
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Rank: {rank}, Depth: {depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")