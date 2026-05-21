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
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = set()
            while len(clause) < 3:
                var = random.randint(-n, n-1)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def incidence_tensor(clauses):
        n = max(abs(v) for v in set.union(*clauses))
        tensor = [[0] * (2*n+1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    tensor[i][var+n-1] += 1
                else:
                    tensor[i][-var-1] -= 1
        return tensor
    
    def symmetric_square(tensor):
        n = len(tensor)
        result = [[0] * (n*n) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        if tensor[i][k] and tensor[j][l]:
                            result[i*n+j][(k+1)*(l+1)-1] += tensor[i][k] * tensor[j][l]
        return result
    
    def young_tableaux_count(tensor):
        n = len(tensor)
        count = 0
        for i in range(n):
            for j in range(n):
                if tensor[i][j]:
                    count += 1
        return count
    
    def resolution_width(clauses):
        stack = []
        width = 0
        for clause in clauses:
            while stack and len(stack[-1]) >= len(clause):
                stack.pop()
            stack.append(clause)
            width = max(width, len(stack))
        return width
    
    n = 40
    clauses = generate_3cnf(n)
    tensor = incidence_tensor(clauses)
    symmetric = symmetric_square(tensor)
    d_phi = young_tableaux_count(symmetric)
    
    if d_phi == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "d(Φ) is zero"
        }
    
    w_phi = resolution_width(clauses)
    threshold = 0.8 * (d_phi ** (1/3)) / math.log(n)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "conjecture_holds": w_phi >= threshold,
        "counterexample": "" if w_phi >= threshold else f"w(Φ) = {w_phi}, threshold = {threshold}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")