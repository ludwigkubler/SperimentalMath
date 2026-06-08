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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        M = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        return M
    
    def rank_variance(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [row[:] for row in M]
        
        # Gaussian elimination
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return float('inf')  # Singular matrix
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        rank = sum(1 for row in A if any(row))
        return (n - rank) / n
    
    def automorphic_forms(M):
        n = len(M)
        forms = set()
        for i in range(n):
            for j in range(n):
                form = [M[(i + k) % n][(j + l) % n] for k in range(n) for l in range(n)]
                forms.add(tuple(form))
        return len(forms)
    
    def correlation_coefficient(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        std_X = math.sqrt(sum((X[i] - mean_X)**2 for i in range(n)) / n)
        std_Y = math.sqrt(sum((Y[i] - mean_Y)**2 for i in range(n)) / n)
        return cov / (std_X * std_Y) if std_X != 0 and std_Y != 0 else float('nan')
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        M = communication_matrix(f)
        rho_f = rank_variance(M)
        if rho_f == float('inf'):
            continue
        aut_f = automorphic_forms(M)
        results.append((aut_f, rho_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    X, Y = zip(*results)
    corr_coef = correlation_coefficient(X, Y)
    p_value = 2 * (1 - math.erf(abs(corr_coef) / math.sqrt(2 * len(results))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coef,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": p_value <= 0.05 and corr_coef >= 0.8,
        "counterexample": "" if corr_coef >= 0.8 else f"corr_coef={corr_coef}, p_value={p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr_coef = sum(result["metric_value"] for result in results) / len(results)
        std_corr_coef = math.sqrt(sum((result["metric_value"] - mean_corr_coef)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coef} std={std_corr_coef} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no data")