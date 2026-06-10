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
    
    def p_adic_analytic_continuation(f, x, p, n):
        # Simplified p-adic analytic continuation for demonstration purposes
        return sum([f(i) * (x ** i) % p for i in range(n)]) % p
    
    def frege_proof_depth(phi):
        # Placeholder function to simulate Frege proof depth calculation
        return len(phi)
    
    def minimal_local_induction_degree(phi):
        # Placeholder function to simulate minimal local induction degree calculation
        return len(phi)
    
    n = random.randint(5, 10)
    d = random.randint(5, 10)
    phi = [random.choice([0, 1]) for _ in range(d)]
    
    p = 2
    n_max = max(n, d)
    growth_rate = 0.0
    lid_values = []
    
    for i in range(30):
        x = random.randint(1, 100)
        cont = p_adic_analytic_continuation(phi, x, p, n_max)
        growth_rate += abs(cont - phi[0])
        lid_values.append(minimal_local_induction_degree(phi))
    
    mean_lid = sum(lid_values) / len(lid_values)
    correlation_coefficient = 0.0
    
    for i in range(len(lid_values)):
        correlation_coefficient += (lid_values[i] - mean_lid) * (growth_rate - growth_rate)
    
    correlation_coefficient /= (len(lid_values) * math.sqrt(sum((x - mean_lid) ** 2 for x in lid_values)) * math.sqrt(growth_rate))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(lid_values),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient < 0.3 for _ in range(1)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")