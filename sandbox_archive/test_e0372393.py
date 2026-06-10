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
    
    def p_adic_analytic_continuation(phi, x, p, n_max):
        f = phi[0]
        for i in range(1, len(phi)):
            f += phi[i] * (x ** i)
        return f % p
    
    def frege_proof_depth(phi):
        if not phi:
            return 0
        return max(frege_proof_depth(sub_phi) for sub_phi in phi) + 1
    
    def minimal_local_induction_degree(phi, n):
        # Placeholder function to compute LID
        return len(phi)
    
    def p_adic_growth_rate(cont, p, n_max):
        growth = [cont(i) for i in range(n_max)]
        return max(abs(growth[i] - growth[i-1]) for i in range(1, len(growth)))
    
    def generate_random_frege_proof(depth, n):
        if depth == 0:
            return random.randint(0, p-1)
        else:
            sub_proofs = [generate_random_frege_proof(random.randint(0, depth-1), n) for _ in range(n)]
            return [sub_proofs]
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    p = 101
    n_max = 40
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(5, 10)
        phi = generate_random_frege_proof(d, n)
        
        depth = frege_proof_depth(phi)
        lid = minimal_local_induction_degree(phi, n)
        
        cont = p_adic_analytic_continuation(phi, 2, p, n_max)
        growth_rate = p_adic_growth_rate(cont, p, n_max)
        
        results.append((lid, growth_rate))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    lids, growth_rates = zip(*results)
    corr = pearson_correlation(lids, growth_rates)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": 0.7 <= corr and corr >= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")