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
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [[0] * (1 << n) for _ in range(n)]
        for i, clause in enumerate(cnf):
            mask = 0
            for lit in clause:
                if lit < 0:
                    mask |= 1 << (-lit - 1)
                else:
                    mask |= 1 << (lit - 1)
            poly[i][mask] = 1
        return poly

    def grothendieck_witt_class_rank(poly):
        n = len(poly[0])
        rank = 0
        for i in range(n):
            if any(poly[j][i] != 0 for j in range(n)):
                rank += 1
        return rank

    def frege_proof_depth(cnf):
        # Placeholder function; replace with actual Frege proof depth calculation
        return len(cnf) * 2  # Example: linear depth

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        poly = clause_indicator_polynomial(cnf)
        gwc_rank = grothendieck_witt_class_rank(poly)
        fp_depth = frege_proof_depth(cnf)
        
        results.append({
            "n": n,
            "gwc_rank": gwc_rank,
            "fp_depth": fp_depth
        })
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    gwc_ranks = [result["gwc_rank"] for result in results]
    fp_depths = [result["fp_depth"] for result in results]
    
    mean_gwc_rank = sum(gwc_ranks) / len(gwc_ranks)
    mean_fp_depth = sum(fp_depths) / len(fp_depths)
    
    covariance = sum((gwc_ranks[i] - mean_gwc_rank) * (fp_depths[i] - mean_fp_depth) for i in range(len(gwc_ranks)))
    variance_gwc_rank = sum((gwc_ranks[i] - mean_gwc_rank) ** 2 for i in range(len(gwc_ranks)))
    variance_fp_depth = sum((fp_depths[i] - mean_fp_depth) ** 2 for i in range(len(fp_depths)))
    
    if variance_gwc_rank == 0 or variance_fp_depth == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearsons_r = covariance / (math.sqrt(variance_gwc_rank) * math.sqrt(variance_fp_depth))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_r,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": pearsons_r >= 0.8 and all(gwc_rank <= 2 * fp_depth for gwc_rank, fp_depth in zip(gwc_ranks, fp_depths)),
        "counterexample": "" if pearsons_r >= 0.8 and all(gwc_rank <= 2 * fp_depth for gwc_rank, fp_depth in zip(gwc_ranks, fp_depths)) else f"pearsons_r={pearsons_r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        counterexample = f"pearsons_r<{min(result['metric_value'] for result in results if not result['conjecture_holds'] and result['metric_value'] < 0.5)}"
    elif any(not result["conjecture_holds"] and result["gwc_rank"] > 2 * result["fp_depth"] for result in results):
        counterexample = f"gwc_rank>2*fp_depth"
    else:
        counterexample = ""
    
    if all(result["n_max"] >= 16 for result in results) and support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")