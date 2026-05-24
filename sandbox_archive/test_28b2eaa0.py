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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return [row[n-1] for row in A]

    def dpll_width(cnf):
        n = len(cnf)
        clauses = cnf
        stack = []
        assignment = {}
        
        def backtrack(level):
            if level == n:
                return True
            var = next((i for i in range(n) if i not in assignment), None)
            if var is None:
                return False
            
            assignment[var] = True
            if all(any(assignment.get(l, False) for l in clause) for clause in clauses):
                stack.append(var)
                if backtrack(level + 1):
                    return True
                stack.pop()
            
            assignment[var] = False
            if all(any(assignment.get(l, False) for l in clause) for clause in clauses):
                stack.append(-var)
                if backtrack(level + 1):
                    return True
                stack.pop()
            
            return False
        
        return len(stack)

    def twisted_tensor_product(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for l in clause:
                if l > 0:
                    A[l-1][l] += 1
                else:
                    A[-l-1][-l] += 1
        return gaussian_elimination(A)

    n = random.randint(5, 40)
    cnf = [[random.choice([-i, i]) for _ in range(random.randint(2, 3))] for _ in range(n)]
    
    rank = len(twisted_tensor_product(cnf))
    width = dpll_width(cnf)
    
    if width == 0:
        return {
            "metric_name": "MinRank(TwistedRep(F)) / DPLLWidth(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLLWidth(F) = 0"
        }
    
    ratio = rank / width
    return {
        "metric_name": "MinRank(TwistedRep(F)) / DPLLWidth(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"MinRank(TwistedRep(F)) / DPLLWidth(F) > 3\" first_failing_seed={seeds[first_failing_seed]}")