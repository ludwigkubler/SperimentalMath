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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        rank = 0
        A_rref = gaussian_elimination(A)
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def dpll_width(formula, assignment={}):
        if not formula:
            return 0
        literals = set()
        for clause in formula:
            literals.update(clause)
        literal = random.choice(list(literals))
        positive_clauses = [c for c in formula if literal in c]
        negative_clauses = [c for c in formula if -literal in c]
        if not positive_clauses and not negative_clauses:
            return 0
        assignment[literal] = True
        width_pos = dpll_width(positive_clauses, assignment)
        del assignment[literal]
        assignment[-literal] = True
        width_neg = dpll_width(negative_clauses, assignment)
        del assignment[-literal]
        return max(width_pos, width_neg) + 1

    def generate_modular_form():
        n = random.randint(5, 40)
        form = []
        for _ in range(n):
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            form.append(clause)
        return form

    formula = generate_modular_form()
    rank = matrix_rank(formula)
    width = dpll_width(formula)

    if rank > 1.5 * width:
        return {
            "metric_name": "Rank/Width Ratio",
            "metric_value": rank / width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula with rank {rank} and width {width}"
        }
    else:
        return {
            "metric_name": "Rank/Width Ratio",
            "metric_value": rank / width,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")