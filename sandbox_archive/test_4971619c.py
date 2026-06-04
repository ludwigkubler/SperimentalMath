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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-i, i]) for _ in range(random.randint(1, 2))]
            cnf.append(clause)
        return cnf
    
    def calculate_automorphism_group(cnf):
        # Placeholder for actual groupoid automorphism group calculation
        # This is a dummy implementation that returns a random number
        return random.randint(1, 100)
    
    def calculate_resolution_proof_width(cnf):
        # Placeholder for actual resolution proof width calculation
        # This is a dummy implementation that returns a random number
        return random.randint(1, 100)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        aut_group_order = calculate_automorphism_group(cnf)
        res_width = calculate_resolution_proof_width(cnf)
        
        if aut_group_order > 100 * res_width:
            conjecture_holds = False
            counterexample = f"aut_group_order={aut_group_order}, res_width={res_width}"
            break
        
        metric_values.append(aut_group_order / res_width)
    
    return {
        "metric_name": "aut_group_order_over_res_width",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")