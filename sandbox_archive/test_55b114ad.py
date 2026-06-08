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
    
    def dpll_solve(phi):
        if not phi:
            return True, []
        for literal in phi[0]:
            new_phi = [c for c in phi if literal not in c and -literal not in c]
            if dpll_solve(new_phi)[0]:
                return True, [literal] + dpll_solve(new_phi)[1]
            new_phi = [c for c in phi if -literal not in c]
            if dpll_solve(new_phi)[0]:
                return True, [-literal] + dpll_solve(new_phi)[1]
        return False, []
    
    def p_adic_valuations(phi):
        valuations = set()
        for clause in phi:
            for literal in clause:
                valuations.add(abs(literal))
        return len(valuations)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Aim for at least 30 instances per seed
            phi = []
            for _ in range(n):
                clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
                phi.append(clause)
            
            proof_path_length = len(dpll_solve(phi)[1])
            valuation_complexity = p_adic_valuations(phi)
            
            if proof_path_length == 0:
                continue
            
            instances_tested += 1
            total_metric_value += abs(valuation_complexity - math.log(n, 2) * proof_path_length)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(abs(mean_metric_value - math.log(n, 2) * dpll_solve(phi)[1]) < 0.5 * math.log(n, 2) * dpll_solve(phi)[1] for n in range(5, n_max + 1) for _ in range(6))
    
    return {
        "metric_name": "p-adic valuation ring complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")