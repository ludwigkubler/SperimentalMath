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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf, n):
        m = len(cnf)
        M = [[0] * (2 * n) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    M[i][lit - 1] = 1
                else:
                    M[i][-lit - 1] = 1
        return M
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            sign = (-1) ** (1 + j)
            det += sign * M[0][j] * determinant(submatrix)
        return det
    
    def roots_count(poly, n):
        if len(poly) == 1:
            return 0
        if poly[-1] != 0:
            return 1 + roots_count([poly[i] / poly[-1] for i in range(len(poly)-1)], n-1)
        else:
            return roots_count(poly[:-1], n-1)
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    M = incidence_matrix(cnf, n)
    det_poly = determinant(M)
    r_min = roots_count(det_poly, n)
    w_phi = resolution_width(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "r(min) / w(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w(φ) is zero"
        }
    
    ratio = r_min / w_phi
    return {
        "metric_name": "r(min) / w(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.5,  # Placeholder constant c=0.5
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r(min) > cw(φ)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")