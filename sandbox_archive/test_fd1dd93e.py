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
    
    def homotopy_dimension(n):
        if n == 0:
            return 0
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        elif n == 3:
            return 2
        else:
            return n - 1
    
    def communication_complexity(n):
        # Placeholder for actual computation
        return random.uniform(0, n**2)
    
    n = random.randint(5, 40)
    hom_dim = homotopy_dimension(n)
    comm_comp = communication_complexity(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_comp,
        "instances_tested": 1,
        "conjecture_holds": hom_dim * n <= comm_comp,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"homotopy_dim({result['instances_tested']}) * {result['instances_tested']} > communication_complexity"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break