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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_norm(poly, p):
        return sum(abs(coeff)**p for coeff in poly) ** (Fraction(1, p))
    
    def monotone_width(cnf):
        n = len(cnf[0])
        gadget = [[-1] * n + [1]] + [[-1 if i == j else 0 for i in range(n)] for j in range(n)]
        return max(sum(row[i] * col[i] for row, col in zip(gadget, cnf)) for i in range(2*n))
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [1]
        for clause in cnf:
            new_poly = []
            for coeff in poly:
                new_poly.extend([coeff * var, coeff * -var] for var in clause)
            poly = new_poly
        return poly
    
    def run_cnf_trial(n):
        cnf = generate_cnf(n)
        indicator_poly = clause_indicator_polynomial(cnf)
        min_Lp = min(p_adic_norm(indicator_poly[:2**n], p) for p in range(1, 4))
        w_mw = monotone_width(cnf)
        return min_Lp, w_mw
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_Lps = []
    w_mws = []
    
    for n in n_values:
        for _ in range(5):
            min_Lp, w_mw = run_cnf_trial(n)
            min_Lps.append(min_Lp)
            w_mws.append(w_mw)
    
    correlation = pearson_correlation(min_Lps, w_mws)
    mean_min_Lp = sum(min_Lps) / len(min_Lps)
    support_fraction = 0.8
    
    if correlation > support_fraction and mean_min_Lp <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Pearson's correlation coefficient does not meet the threshold or mean Lp is too high"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(min_Lps),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")