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
    
    def generate_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def local_cohomology_degree(formula):
        n = len(formula)
        h = 0
        for i in range(n):
            count = sum(1 for j in range(n) if formula[j] == i % 2)
            h += count * (count - 1) // 2
        return h
    
    def resolution_proof_width(formula):
        n = len(formula)
        width = 0
        for i in range(n):
            if formula[i] == 1:
                width += 1
        return width
    
    instances_tested = 0
    total_h = 0
    total_w = 0
    n_max = 5
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        formula = generate_formula(n)
        h = local_cohomology_degree(formula)
        w = resolution_proof_width(formula)
        
        total_h += h
        total_w += w
        instances_tested += 1
    
    mean_h = total_h / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(h * w for h, w in zip([local_cohomology_degree(generate_formula(n)) for n in range(5, 41)], [resolution_proof_width(generate_formula(n)) for n in range(5, 41)])) - instances_tested * mean_h * mean_w) / (instances_tested * sum((h - mean_h)**2 for h in [local_cohomology_degree(generate_formula(n)) for n in range(5, 41)]) * sum((w - mean_w)**2 for w in [resolution_proof_width(generate_formula(n)) for n in range(5, 41)]))
    
    slope = correlation_coefficient * (mean_h / instances_tested)
    
    conjecture_holds = correlation_coefficient > 0.5 and slope >= 1.2 * math.log(n_max) / mean_h**2
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_w,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_w = sum(r["metric_value"] for r in results) / len(results)
    std_w = math.sqrt(sum((r["metric_value"] - mean_w)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_w} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={next(r['seed'] for r in results if not r['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")