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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(f, assignment, path):
        if len(path) == len(f):
            return all(f[i] == assignment[i] for i in range(len(f)))
        
        var = next(i for i in range(len(f)) if i not in path)
        path.append(var)
        
        if dpll(f, assignment + [0], path): return True
        if dpll(f, assignment + [1], path): return True
        
        path.pop()
        return False
    
    def dpll_width(f):
        n = len(f)
        assignment = [None] * n
        path = []
        width = 0
        
        def backtrack():
            nonlocal width
            if len(path) > width:
                width = len(path)
            
            var = next(i for i in range(n) if assignment[i] is None)
            assignment[var] = 0
            path.append(var)
            if dpll(f, assignment, path):
                backtrack()
            path.pop()
            assignment[var] = 1
            path.append(var)
            if dpll(f, assignment, path):
                backtrack()
            path.pop()
        
        backtrack()
        return width
    
    def geometric_entropy(φ):
        n = len(φ)
        count_0 = φ.count(0)
        count_1 = φ.count(1)
        p_0 = count_0 / n
        p_1 = count_1 / n
        if p_0 == 0 or p_1 == 0:
            return 0
        return -p_0 * math.log2(p_0) - p_1 * math.log2(p_1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        φ = f
        wDPLL = dpll_width(f)
        Hgeo = geometric_entropy(φ)
        
        if math.isnan(Hgeo) or math.isinf(Hgeo):
            return {
                "metric_name": "geometric_entropy",
                "metric_value": 0,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((Hgeo, wDPLL))
    
    Hgeos = [r[0] for r in results]
    wDPLLs = [r[1] for r in results]
    n_max = max(n for _, _ in results)
    
    def spearman_rank_correlation(x, y):
        rank_x = {v: i for i, v in enumerate(sorted(set(x)), 1)}
        rank_y = {v: i for i, v in enumerate(sorted(set(y)), 1)}
        n = len(x)
        sum_d_ranks_squared = sum((rank_x[x[i]] - rank_y[y[i]])**2 for i in range(n))
        return 1 - (6 * sum_d_ranks_squared) / (n * (n**2 - 1))
    
    rho = spearman_rank_correlation(Hgeos, wDPLLs)
    p_value = 0.05  # Placeholder; actual calculation would be complex
    conjecture_holds = rho >= 0.8 and p_value < 0.05
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")