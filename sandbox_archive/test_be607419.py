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
    
    def inner_product_mod_2(x, y):
        return sum(int(a) * int(b) % 2 for a, b in zip(x, y))
    
    def trivial_bp(n):
        return [[inner_product_mod_2(bin(i)[2:].zfill(n), bin(j)[2:].zfill(n)) for j in range(1 << n)] for i in range(1 << n)]
    
    def tropicalized_hodge_decomposition(P):
        # Simplified version of the Hodge decomposition
        return sum(sum(row) for row in P)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        s_P = len(trivial_bp(n)) ** 2
        rho_H_P = tropicalized_hodge_decomposition(trivial_bp(n))
        results.append({
            "n": n,
            "s_P": s_P,
            "rho_H_P": rho_H_P,
            "ratio": abs(rho_H_P - math.log(s_P)),
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    max_rho_H_P = max(result["rho_H_P"] for result in results)
    support_fraction = all(result["ratio"] <= 0.1 for result in results)
    
    return {
        "metric_name": "Ratio |ρ_H(P) - log(s(P))|",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction and max_rho_H_P <= math.log(max([result["s_P"] for result in results])) + 1,
        "counterexample": "" if support_fraction else f"max_rho_H_P={max_rho_H_P} > log(s(P)) + 1",
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    max_rho_H_P = max(result["counterexample"].split("=")[1].strip() if result["conjecture_holds"] else 0 for result in results)
    support_fraction = all("support" in result["counterexample"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif max_rho_H_P > 0:
        print(f"RESULT: FALSIFIED counterexample='max_rho_H_P={max_rho_H_P} > log(s(P)) + 1' first_failing_seed={seeds[results.index(next(result for result in results if 'falsified' in result["counterexample"] and 'support' not in result["counterexample"]))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")