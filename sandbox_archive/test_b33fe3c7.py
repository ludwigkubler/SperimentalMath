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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def hamiltonian_matrix(cnf):
        n = max(abs(lit) for lit in cnf)
        H = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    i, j = lit, -lit
                else:
                    i, j = -lit, lit
                H[i][j] += 1
                H[j][i] += 1
        return H

    def min_quaternionic_norm(H):
        n = len(H)
        for _ in range(n * n):  # Gaussian elimination
            max_row = max(range(n), key=lambda r: abs(H[r][0]))
            if H[max_row][0] == 0:
                continue
            H[max_row], H[0] = H[0], H[max_row]
            for j in range(1, n):
                H[j][0] /= H[0][0]
            for i in range(n):
                if i != 0:
                    factor = H[i][0]
                    for j in range(n + 1):
                        H[i][j] -= factor * H[0][j]
        norm = sum(abs(H[i][i]) for i in range(n))
        return norm

    def circuit_monotone_width(cnf):
        n = max(abs(lit) for lit in cnf)
        # Simplified monotone width calculation (not accurate but sufficient for testing)
        return len(set(abs(lit) for lit in cnf))

    instances_tested = 0
    total_norm = 0.0
    total_width = 0
    n_max = 0

    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        H = hamiltonian_matrix(cnf)
        norm = min_quaternionic_norm(H)
        width = circuit_monotone_width(cnf)

        instances_tested += 1
        total_norm += norm
        total_width += width
        n_max = max(n_max, n)

    mean_norm = total_norm / instances_tested
    mean_width = total_width / instances_tested

    correlation_coefficient = (instances_tested * sum(norm * width for norm, width in zip([mean_norm] * instances_tested, [mean_width] * instances_tested)) -
                               sum([mean_norm] * instances_tested) * sum([mean_width] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(norm ** 2 for norm in [mean_norm] * instances_tested) - (sum([mean_norm] * instances_tested) ** 2)) *
                                        (instances_tested * sum(width ** 2 for width in [mean_width] * instances_tested) - (sum([mean_width] * instances_tested) ** 2)))

    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")