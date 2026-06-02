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
    
    def frobenius_monomial_rank(formula):
        # Placeholder implementation for Frobenius monomial rank
        return len(formula.split('&'))
    
    def frege_proof_length(formula):
        # Placeholder implementation for Frege proof length
        if formula.startswith('(&') and formula.endswith(')'):
            left, right = formula[2:-1].split('&')
            return max(frege_proof_length(left), frege_proof_length(right)) + 1
        else:
            return 1
    
    def frobenius_algebraic_operation(formula):
        # Placeholder implementation for Frobenius algebraic operation
        if formula.startswith('(&') and formula.endswith(')'):
            left, right = formula[2:-1].split('&')
            new_formula = f'({left} & {right})'
            return frobenius_algebraic_operation(new_formula)
        else:
            return formula
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    instances_tested = 0
    mfr_values = []
    l_values = []
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = '(&' + '&'.join(random.choices(['x', 'y'], k=n)) + ')'
            mfr = frobenius_monomial_rank(formula)
            l = frege_proof_length(formula)
            if len(mfr_values) >= 30:
                break
            mfr_values.append(mfr)
            l_values.append(l)
            instances_tested += 1
    
    correlation_coefficient = pearson_correlation(mfr_values, l_values)
    
    conjecture_holds = correlation_coefficient >= 0.8
    
    if not conjecture_holds:
        counterexample = "Frobenius monomial rank and Frege proof length are not linearly correlated"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius monomial rank and Frege proof length are not linearly correlated\" first_failing_seed={first_failing_seed}")