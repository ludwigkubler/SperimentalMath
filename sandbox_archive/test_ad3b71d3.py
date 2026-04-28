# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def lex_dpll(F):
    def dpll(F, assignment):
        if not F:
            return True
        unit_clauses = [c for c in F if len(c) == 1]
        if unit_clauses:
            v = unit_clauses[0][0]
            if v < 0 and -v in assignment and assignment[-v]:
                return False
            elif v > 0 and v not in assignment:
                assignment[v] = True
            else:
                assignment[v] = False
        pure_literals = [v for v in range(1, max(F) + 1) if all(v in c or -v in c for c in F)]
        if pure_literals:
            v = pure_literals[0]
            if v not in assignment:
                assignment[v] = True
            else:
                assignment[v] = False
        for literal in range(1, max(F) + 1):
            if literal not in assignment and -literal not in assignment:
                return dpll(F, {**assignment, literal: True}) or dpll(F, {**assignment, literal: False})
        return False

    return dpll(F, {})

def grundy_value(F, memo):
    F = [tuple(sorted(c)) for c in F]
    if tuple(sorted(F)) in memo:
        return memo[tuple(sorted(F))]
    if not F:
        return 0
    moves = set()
    for clause in F:
        for literal in clause:
            new_F = [c for c in F if literal not in c and -literal not in c]
            new_F = [tuple(sorted(c)) for c in new_F]
            moves.add(grundy_value(new_F, memo))
    mex = 0
    while mex in moves:
        mex += 1
    memo[tuple(sorted(F))] = mex
    return mex

def generate_cnf(n, alpha):
    F = []
    variables = set(range(1, n + 1))
    for _ in range(int(alpha * n * (n - 1) / 2)):
        v1, v2 = random.sample(variables, 2)
        literals = [v1, -v1, v2, -v2]
        random.shuffle(literals)
        F.append(tuple(literals))
    return F

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    alpha_values = [4.5, 5.0, 5.5]
    memo = defaultdict(int)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            F = generate_cnf(n, alpha)
            if lex_dpll(F):
                continue
            G_F = grundy_value(F, memo)
            L_T = lex_dpll([tuple(sorted(c)) for c in F], {})
            instances_tested += 1
            if not (math.floor(math.log2(1 + G_F)) <= math.ceil(math.log2(L_T))):
                conjecture_holds = False
                counterexample = f"n={n}, alpha={alpha}, G(F)={G_F}, L_T={L_T}"
                break

    return {
        "metric_name": "log2_GF_vs_log2_LT",
        "metric_value": math.log2(1 + grundy_value(generate_cnf(10, 5.0), memo)) if instances_tested > 0 else None,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")