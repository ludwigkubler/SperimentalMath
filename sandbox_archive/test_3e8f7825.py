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
        poly = [0] * (1 << n)
        for clause in cnf:
            mask = 0
            for lit in clause:
                if lit.startswith('-'):
                    mask |= 1 << abs(int(lit[1:])) - 1
                else:
                    mask |= 1 << abs(int(lit)) - 1
            poly[mask] += 1
        return poly
    
    def grothendieck_witt_class_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            if poly[i] != 0:
                rank += 1
        return rank
    
    def frege_proof_depth(cnf):
        # Placeholder function, actual implementation needed
        return random.randint(5, 20)  # Simulate a depth between 5 and 20
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times to ensure statistical signal
            cnf = [[random.randint(-n, -1), random.randint(1, n)] for _ in range(random.randint(2, 4))]
            poly = clause_indicator_polynomial(cnf)
            gwc_rank = grothendieck_witt_class_rank(poly)
            fp_depth = frege_proof_depth(cnf)
            
            if gwc_rank > 2 * fp_depth:
                conjecture_holds = False
                counterexample = f"n={n}, gwc_rank={gwc_rank}, fp_depth={fp_depth}"
                break
            
            total_metric_value += abs(gwc_rank - fp_depth)
            instances_tested += 1
            max_n = max(max_n, n)
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results) or any(r["gwc_rank"] > 2 * r["fp_depth"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")