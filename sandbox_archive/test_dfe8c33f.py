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
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x

    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        if a < 0:
            a += p
        return pow(a, (p - 1) // 2, p) == 1

    def count_quadratic_residues(p):
        return sum(is_quadratic_residue(a, p) for a in range(1, p))

    def dpll(cnf):
        if not cnf:
            return True
        for literal in cnf[0]:
            new_cnf = [clause.copy() for clause in cnf]
            for clause in new_cnf:
                if literal in clause:
                    clause.remove(literal)
                elif -literal in clause:
                    clause.remove(-literal)
                    break
            else:
                return dpll(new_cnf) or dpll([c + [-literal] for c in new_cnf])
        return False

    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            variables = random.sample(range(1, 2 * n + 1), 3)
            clause = [random.choice([-1, 1]) * v for v in variables]
            clauses.append(clause)
        return clauses

    def order_of_multiplicative_group(p):
        if p <= 1:
            raise ValueError("p must be greater than 1")
        phi_p = p - 1
        factors = []
        for i in range(2, int(math.sqrt(phi_p)) + 1):
            while phi_p % i == 0:
                factors.append(i)
                phi_p //= i
        if phi_p > 1:
            factors.append(phi_p)
        return math.lcm(*factors)

    n = 30
    cnf = generate_cnf(n)
    p = order_of_multiplicative_group(2 * n + 1)
    residues_count = count_quadratic_residues(p)
    log_residues = math.log(residues_count, 2)
    
    if residues_count == 0:
        return {
            "metric_name": "DPLL search tree height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dpll_height = len(gaussian_elimination([[random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)] for _ in range(n)], [0] * n))
    
    return {
        "metric_name": "DPLL search tree height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(dpll_height - log_residues) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")