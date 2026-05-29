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
    
    def k_cnf_formula(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < n:
                var = random.randint(1, 2*n)
                if var not in clause:
                    clause.add(var)
            clauses.append(clause)
        return clauses

    def incidence_matrix(clauses, n):
        W_n = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                if 2*i + 1 in clause:
                    W_n[i][i] += 1
                elif 2*i + 2 in clause:
                    W_n[i][i] -= 1
        return W_n

    def schur_weyl_polynomial(W_n):
        n = len(W_n)
        det = 0
        for perm in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j and perm[i] > perm[j] for i, j in itertools.combinations(range(n), 2))
            product = 1
            for i in range(n):
                product *= W_n[perm[i]][i]
            det += sign * product
        return abs(det)

    def monomial_ideal_complexity(clauses, n):
        # Placeholder function; actual implementation needed
        return len(clauses) ** 2

    n = random.randint(5, 40)
    k = random.randint(3, min(n - 1, 10))
    clauses = k_cnf_formula(n, k)
    W_n = incidence_matrix(clauses, n)
    rho_W_n = schur_weyl_polynomial(W_n)
    I_m_k_n = monomial_ideal_complexity(clauses, n)

    if I_m_k_n == 0:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "I_m(k,n) is zero"
        }

    rho_W_n_1_5 = rho_W_n ** 1.5
    spearman_corr_coeff = (2 * sum((rank(clauses[i], clauses[j]) - 0.5) for i in range(n) for j in range(i + 1, n)) /
                           (n * (n - 1)))

    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": spearman_corr_coeff,
        "instances_tested": 1,
        "conjecture_holds": spearman_corr_coeff >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")