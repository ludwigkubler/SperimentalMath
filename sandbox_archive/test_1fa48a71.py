# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_generators(f):
        n = len(f)
        if n == 1:
            return 1
        points = set()
        for x in range(2**(n-1)):
            y = f[x]
            points.add((x, y))
        return len(points)
    
    total_generators = 0
    instances_tested = 30
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        generators = count_generators(f)
        total_generators += generators
    
    average_generators = Fraction(total_generators, instances_tested)
    conjecture_holds = average_generators >= Fraction(2**n, 4)
    counterexample = "" if conjecture_holds else f"Average generators {average_generators} < {Fraction(2**n, 4)}"
    
    return {
        "metric_name": "average_generators",
        "metric_value": float(average_generators),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    total_generators = 0
    instances_tested_total = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_generators += trial_result["metric_value"] * trial_result["instances_tested"]
        instances_tested_total += trial_result["instances_tested"]
    
    mean_generators = Fraction(total_generators, instances_tested_total)
    support_fraction = sum(1 for seed in seeds if run_trial(seed)["conjecture_holds"]) / len(seeds)
    
    if support_fraction >= 0.8:
        result = f"SUPPORTED mean={mean_generators} std=NA support_fraction={support_fraction}"
    elif any(not run_trial(seed)["conjecture_holds"] for seed in seeds):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"{run_trial(first_failing_seed)['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE insufficient data"
    
    print(result)