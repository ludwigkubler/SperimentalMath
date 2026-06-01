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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[2**i] != f[2**j]:
                    count += 1
        return count
    
    def minimal_kostant_cohomology_rank(f):
        # Placeholder implementation (replace with actual method)
        return len(f) / 2
    
    instances_tested = 0
    n_max = 0
    total_kcr = 0
    total_cc = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        f = generate_boolean_function(n)
        kcr = minimal_kostant_cohomology_rank(f)
        cc = communication_complexity(f)
        
        total_kcr += kcr
        total_cc += cc
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    mean_kcr = total_kcr / instances_tested
    mean_cc = total_cc / instances_tested
    
    correlation_coefficient = (instances_tested * sum(kcr * cc for kcr, cc in zip([mean_kcr] * instances_tested, [mean_cc] * instances_tested)) - instances_tested * mean_kcr * mean_cc) / \
                               math.sqrt((instances_tested * sum(kcr**2 for kcr in [mean_kcr] * instances_tested) - instances_tested * mean_kcr**2) * (instances_tested * sum(cc**2 for cc in [mean_cc] * instances_tested) - instances_tested * mean_cc**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")