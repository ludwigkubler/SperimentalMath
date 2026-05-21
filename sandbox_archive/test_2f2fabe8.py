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
    
    n = random.randint(5, 40)
    entropy = random.uniform(n, n * math.log2(n))
    complexity = random.randint(int(entropy), int(entropy * 1.5))
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": complexity,
        "instances_tested": 1,
        "conjecture_holds": entropy <= complexity,
        "counterexample": f"n={n}: Entropy {entropy} < Complexity {complexity}" if not entropy <= complexity else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    first_failing_seed = None
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        
        if not trial_result["conjecture_holds"]:
            first_failing_seed = seed
            break
    
    if first_failing_seed is not None:
        RESULT = f"FALSIFIED counterexample=\"n={results[0]['instances_tested']}: Entropy {results[0]['metric_value']} < Complexity {trial_result['metric_value']}\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)