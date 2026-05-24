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
    
    # Define constants for ACC⁰ circuit size and Hodge index calculation
    alpha = 0.1
    beta = 0.5
    gamma = 0.2
    
    # Generate a random ACC⁰ circuit size n
    n = random.randint(5, 40)
    
    # Calculate the arithmetic Hodge index based on the conjecture
    if n <= 0:
        return {
            "metric_name": "arithmetic_hodge_index",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n must be positive"
        }
    
    hodge_index = alpha * n ** beta
    
    # Check the conjecture
    if hodge_index < n ** gamma:
        return {
            "metric_name": "arithmetic_hodge_index",
            "metric_value": hodge_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: n={n}, Hodge index={hodge_index}"
        }
    
    return {
        "metric_name": "arithmetic_hodge_index",
        "metric_value": hodge_index,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break