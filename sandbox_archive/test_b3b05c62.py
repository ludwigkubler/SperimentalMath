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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank_matrix(A):
        if not A:
            return 0
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if A[i][i]:
                rank += 1
                for j in range(i + 1, m):
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.randint(1, 2) * random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def communication_complexity_rank_variance(phi):
        # Simplified DPLL solver to estimate RC(φ)
        count = 0
        for assignment in itertools.product([True, False], repeat=len(phi)):
            if all(any(not (x < 0 and not assignment[-x]) for x in clause) for clause in phi):
                count += 1
        return Fraction(count, 2 ** len(phi))
    
    n = random.randint(5, 40)
    phi = generate_cnf(n)
    mrank_phi = rank_matrix(gaussian_elimination(phi))
    if mrank_phi is None:
        return {
            "metric_name": "mrank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    rc_phi = communication_complexity_rank_variance(phi)
    return {
        "metric_name": "mrank",
        "metric_value": mrank_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_mrank = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_mrank)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = result.get("counterexample", "")
        mean_mrank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
        std_dev = math.sqrt(sum((r["metric_value"] - mean_mrank)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mrank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")