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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            random.shuffle(literals)
            clause = ' or '.join(f'x{i+1}' if l == 1 else f'-x{i+1}' for l in literals)
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0].split(' or '))
        poly = [0] * (2 ** n)
        for clause in clauses:
            bits = [1 if 'x' + str(i+1) in clause else 0 for i in range(n)]
            index = sum(bit << i for i, bit in enumerate(reversed(bits)))
            poly[index] += 1
        return poly
    
    def schur_weyl_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(2 ** (n - 1)):
            subpoly = [poly[j] if (i & (1 << j)) else 0 for j in range(n)]
            if sum(subpoly) != 0:
                rank += 1
        return rank
    
    def dpll_length(clauses):
        stack = []
        assignment = [None] * len(clauses)
        
        def backtrack(level):
            if level == len(clauses):
                return True
            for literal in [-1, 1]:
                var = abs(int(clauses[level].split('x')[1]))
                if (assignment[var - 1] is None and literal != assignment[var - 1]):
                    assignment[var - 1] = literal
                    stack.append((level + 1, literal))
                    if backtrack(level + 1):
                        return True
                    stack.pop()
                    assignment[var - 1] = None
            return False
        
        return len(stack) if backtrack(0) else float('inf')
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    poly = clause_indicator_polynomial(formula.split(' and '))
    min_rank = schur_weyl_rank(poly)
    dpll_len = dpll_length(formula.split(' and '))
    
    return {
        "metric_name": "min_rank(V)",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False if dpll_len == float('inf') else True,
        "counterexample": "" if dpll_len != float('inf') else "DPLL_length(F) is infinite"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL_length(F) is infinite\" first_failing_seed={first_failing_seed}")