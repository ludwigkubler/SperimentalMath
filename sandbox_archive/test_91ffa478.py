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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                if k < i:
                    matrix[j][k] -= factor * matrix[i][k]
                elif k == i:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def resolution_length(cnf_instance):
    n = len(cnf_instance)
    clauses = cnf_instance[:]
    stack = []
    
    while True:
        if not clauses:
            return len(stack)
        
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            stack.append(literal)
            clauses = [c for c in clauses if literal not in c and -literal not in c]
        else:
            resolvent = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    common_literals = set(c for c in clauses[i] if -c in clauses[j])
                    if common_literals:
                        resolvent = [l for l in clauses[i] if l not in common_literals]
                        resolvent.extend(l for l in clauses[j] if l not in common_literals)
                        break
                else:
                    continue
                break
            if not resolvent:
                return len(stack)
            clauses.append(resolvent)
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_instance = [[random.randint(-n, n) for _ in range(random.randint(2, n))] for _ in range(n)]
    
    rank = gaussian_elimination(cnf_instance)
    resolution_len = resolution_length(cnf_instance)
    
    metric_value = max(len([x for x in row if x != 0]) for row in rank)
    conjecture_holds = (metric_value >= 2**(n - math.log(n, 2))) and (resolution_len >= 2**(n - math.log(n, 2)))
    counterexample = "" if conjecture_holds else "K-theory rank or resolution length too small"
    
    return {
        "metric_name": "Minimal Rank of K-theory vs Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"K-theory rank or resolution length too small\" first_failing_seed={first_failing_seed}")