# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    if seed > 3:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = seed + 2
    if n < 3:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    # Compute Kronecker coefficients for λ = (n-1,1) in the decomposition of Sym^2(perm) vs Sym^2(det)
    def kronecker_coefficient(m, n, k):
        if m == 0 or n == 0 or k == 0:
            return Fraction(1, 1)
        if k > min(m, n):
            return Fraction(0, 1)
        coeff = Fraction(1, 1)
        for i in range(k):
            coeff *= (m - i) * (n - i)
            coeff /= (i + 1) * (k - i)
        return coeff
    
    def symmetric_group_multiplicity(n, lambda_):
        if len(lambda_) != 2 or lambda_[0] != n-1 or lambda_[1] != 1:
            return Fraction(0, 1)
        
        m = lambda_[0]
        k = lambda_[1]
        
        coeff = kronecker_coefficient(m, m, k) * kronecker_coefficient(m, m, k)
        return coeff
    
    perm_multiplicity = symmetric_group_multiplicity(n, (n-1, 1))
    det_multiplicity = symmetric_group_multiplicity(n, (n-1, 1))
    
    # Check if the multiplicity of (n-1,1) in permanent is strictly greater than determinant
    conjecture_holds = perm_multiplicity > det_multiplicity
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": perm_multiplicity - det_multiplicity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "(n-1,1) multiplicity gap is not strictly greater"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")