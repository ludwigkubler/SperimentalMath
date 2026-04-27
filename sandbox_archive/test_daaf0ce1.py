# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def van_der_corput_base2(n):
    if n == 0:
        return 0.5
    else:
        vdc = 0.0
        factor = 0.5
        while n > 0:
            remainder = n % 2
            vdc += remainder * factor
            factor /= 2
            n //= 2
        return vdc

def generate_3cnf(n, alpha):
    m = int(alpha * n**3 / 6)
    clauses = []
    for _ in range(m):
        literals = set()
        while len(literals) < 3:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            literals.add(sign * var)
        clauses.append(tuple(sorted(literals)))
    return clauses

def dpll(F, assignment):
    if not F:
        return True
    clause = next((c for c in F if any(l in assignment and assignment[l] == (l > 0) for l in c)), None)
    if not clause:
        return False
    p = next((l for l in clause if l > 0), None)
    if p is None:
        q = -next((l for l in clause if l < 0), None)
        assignment[q] = True
        if dpll(F, assignment):
            return True
        del assignment[q]
        assignment[q] = False
        if dpll(F, assignment):
            return True
        del assignment[q]
    else:
        assignment[p] = True
        if dpll(F, assignment):
            return True
        del assignment[p]
        assignment[p] = False
        if dpll(F, assignment):
            return True
        del assignment[p]
    return False

def count_dpll_leaves(F):
    def dfs(F, assignment):
        if not F:
            return 1
        clause = next((c for c in F if any(l in assignment and assignment[l] == (l > 0) for l in c)), None)
        if not clause:
            return 0
        p = next((l for l in clause if l > 0), None)
        if p is None:
            q = -next((l for l in clause if l < 0), None)
            assignment[q] = True
            leaves1 = dfs(F, assignment)
            del assignment[q]
            assignment[q] = False
            leaves2 = dfs(F, assignment)
            del assignment[q]
        else:
            assignment[p] = True
            leaves1 = dfs(F, assignment)
            del assignment[p]
            assignment[p] = False
            leaves2 = dfs(F, assignment)
            del assignment[p]
        return leaves1 + leaves2
    return dfs(F, {})

def star_discrepancy(points):
    n = len(points)
    m = int(math.ceil(4 * math.log(n) / 3))
    boxes = [[0] * 3 for _ in range(m)]
    for p in points:
        i = int(p[0] * (2**m)) % m
        j = int(p[1] * (2**m)) % m
        k = int(p[2] * (2**m)) % m
        boxes[i][0] += 1
        boxes[j][1] += 1
        boxes[k][2] += 1
    max_discrepancy = 0
    for box in boxes:
        max_discrepancy = max(max_discrepancy, abs(box[0] - n / (2**m)), abs(box[1] - n / (2**m)), abs(box[2] - n / (2**m)))
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    alpha = 4.267
    results = []
    for n in [10, 12, 14, 16, 18, 20]:
        F = generate_3cnf(n, alpha)
        if dpll(F, {}):
            continue
        points = [(van_der_corput_base2(sign * var + n) for sign in [1, -1] for var in range(1, n + 1)) for _ in range(len(F))]
        D_F = star_discrepancy(points)
        L_F = count_dpll_leaves(F)
        results.append((n, D_F, L_F))
    metric_value = sum(L_F * math.log2(D_F) for n, D_F, L_F in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(0.5 * n * D_F - 5 <= math.log2(L_F) <= 4 * n * D_F + 5 for _, D_F, L_F in results)
    counterexample = "" if conjecture_holds else "log2 L(F) < 0.4*n*D*(F) - 5 with n<=20"
    return {
        "metric_name": "log2 L(F)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and n <= 20 for r, n in zip(results, [10, 12, 14, 16, 18, 20])):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and any(n <= 20 for _, n in zip(results, [10, 12, 14, 16, 18, 20])))
        print(f"RESULT: FALSIFIED counterexample=\"log2 L(F) < 0.4*n*D*(F) - 5 with n<=20\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")