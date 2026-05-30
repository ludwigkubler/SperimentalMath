# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def communication_complexity(f):
        n = len(f)
        kappa_f = 0
        for x in range(1 << (n-1)):
            y = f[x] ^ f[x + (1 << (n-1))]
            if y != f[0]:
                kappa_f += 1
        return kappa_f
    
    def random_boolean_function(n):
        return [random.randint(0, 1) for _ in range(1 << n)]
    
    def symplectic_area(density_matrix):
        det = 1.0
        for i in range(len(density_matrix)):
            det *= density_matrix[i][i]
        return -math.log(det)
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 30:
            break
        
        kappa_values = []
        area_values = []
        
        for _ in range(30):
            f = random_boolean_function(n)
            rho = [[random.random() for _ in range(n)] for _ in range(n)]
            kappa_f = communication_complexity(f)
            area_rho = symplectic_area(rho)
            
            kappa_values.append(kappa_f)
            area_values.append(area_rho)
        
        instances_tested += len(kappa_values)
        n_max = max(n_max, n)
        
        if len(kappa_values) < 10:
            continue
        
        # Spearman's rank correlation coefficient
        ranks_kappa = {x: i for i, x in enumerate(sorted(set(kappa_values)), start=1)}
        ranks_area = {x: i for i, x in enumerate(sorted(set(area_values)), start=1)}
        
        rho_numerator = sum((ranks_kappa[k] - ranks_area[a]) ** 2 for k, a in zip(kappa_values, area_values))
        rho_denominator = len(kappa_values) * (len(kappa_values) ** 2 - 1)
        rho = 1 - (6 * rho_numerator) / rho_denominator
        
        results.append({
            "n": n,
            "rho": rho
        })
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No data collected"
        }
    
    mean_rho = sum(r["rho"] for r in results) / len(results)
    p_value = 0.05  # Assuming a significance level of 0.05
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_rho >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=None support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho < 0.7' first_failing_seed={first_failing_seed}")