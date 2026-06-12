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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def p_adic_log(x, p):
        if x <= 0:
            return None
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate width
        clauses = phi.split(' and ')
        literals = set()
        for clause in clauses:
            literals.update(clause.split(' or '))
        return len(literals)
    
    def minimal_p_adic_root_divergence(phi, p):
        clauses = phi.split(' and ')
        indicators = [0] * len(clauses)
        for i, clause in enumerate(clauses):
            if 'true' in clause:
                indicators[i] = 1
            elif 'false' in clause:
                indicators[i] = -1
        
        A = []
        b = []
        for i in range(len(indicators)):
            row = [indicators[j] for j in range(i+1, len(indicators))]
            A.append(row)
            b.append(indicators[i])
        
        solution = gaussian_elimination(A, b)
        distances = [abs(solution[i] - solution[j]) for i in range(len(solution)) for j in range(i+1, len(solution))]
        if not distances:
            return 0
        return p_adic_log(min(distances), p)
    
    def generate_formula(n):
        variables = 'x' + ''.join(str(i) for i in range(1, n+1))
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append('not ' + variables[j])
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    p = 2
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    mrd_sum = 0
    w_sum = 0
    
    for n in n_values:
        for _ in range(5):
            phi = generate_formula(n)
            if 'true' not in phi and 'false' not in phi:
                continue
            instances_tested += 1
            mrd = minimal_p_adic_root_divergence(phi, p)
            w = resolution_width(phi)
            if mrd is None or w == 0:
                continue
            mrd_sum += mrd
            w_sum += w
    
    if instances_tested < 30:
        return {
            "metric_name": "mrd vs w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_mrd = mrd_sum / instances_tested
    mean_w = w_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(mrd * w for mrd, w in zip([mrd_sum / instances_tested] * instances_tested, [w_sum / instances_tested] * instances_tested)) - mrd_sum * w_sum) / (math.sqrt(instances_tested * sum((mrd - mean_mrd)**2 for mrd in [mrd_sum / instances_tested] * instances_tested)) * math.sqrt(instances_tested * sum((w - mean_w)**2 for w in [w_sum / instances_tested] * instances_tested)))
    
    return {
        "metric_name": "mrd vs w",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": 0.7 <= correlation_coefficient <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**i + 5**i for i in range(1, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")