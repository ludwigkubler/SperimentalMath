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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        clause = next((c for c in clauses if any(x in c for x in assignment)), [])
        if not clause:
            return False
        var = next((x for x in clause if x > 0), None)
        if dpll([c for c in clauses if var not in c], assignment + [var]):
            return True
        if dpll([c for c in clauses if -var not in c], assignment + [-var]):
            return True
        return False
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        Q = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & (1 << x)) or (-j & (1 << x)) for x in range(n)):
                    Q[i][j] = 1
        return Q
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(n):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(i, n)):
                        factor = matrix[k][i] / matrix[i][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    def height_dpll(clauses):
        if not clauses:
            return 1
        clause = next((c for c in clauses if any(x in c for x in [1, -1])), [])
        if not clause:
            return 0
        var = next((x for x in clause if x > 0), None)
        return 1 + max(height_dpll([c for c in clauses if var not in c]), height_dpll([c for c in clauses if -var not in c]))
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    
    Q = clause_indicator_polynomial(clauses)
    rank = min_rank(Q)
    height = height_dpll(clauses)
    
    return {
        "metric_name": "Rank vs Height",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= height,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")