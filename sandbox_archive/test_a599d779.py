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
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def compute_clause_indicator_polynomial(clauses, n):
        polynomial = [0] * (2 ** n)
        for clause in clauses:
            product = 1
            for var in clause:
                product *= (-1) ** random.choice([0, 1])
            polynomial[sum(1 << (n - 1 - i) for i in clause)] += product
        return polynomial
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                pivot_found = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        pivot_found = True
                        break
                if not pivot_found:
                    continue
            rank += 1
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n + 1):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def dpll_search_tree_width(clauses, n):
        # Simplified heuristic to estimate DPLL search tree width
        return len(max([len(c) for c in clauses], default=0))
    
    n = random.randint(5, 40)
    clauses = generate_sat_instance(n)
    polynomial = compute_clause_indicator_polynomial(clauses, n)
    matrix = [[polynomial[1 << i | 1 << j] - polynomial[1 << i] - polynomial[1 << j] + polynomial[0] for j in range(n)] for i in range(n)]
    minimal_rank = gaussian_elimination(matrix)
    dpll_width = dpll_search_tree_width(clauses, n)
    
    f_n = math.sqrt(n) * math.log(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= f_n and dpll_width > 0,
        "counterexample": "" if minimal_rank <= f_n else f"n={n}, rank={minimal_rank}, width={dpll_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds f(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")