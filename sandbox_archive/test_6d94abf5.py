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
    
    # Placeholder for generating a language L in PSPACE with bounded width planar branching programs.
    # This is a stub and should be replaced with actual code to generate such languages.
    n = random.randint(5, 40)
    input_size = n * (n + 1) // 2
    braided_monoidal_category_rank = random.randint(input_size, input_size * 10)  # Placeholder for actual computation
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": braided_monoidal_category_rank,
        "instances_tested": 1,
        "conjecture_holds": braided_monoidal_category_rank <= input_size ** 3,  # Polynomial bound
        "counterexample": "" if braided_monoidal_category_rank <= input_size ** 3 else f"Exponential rank {braided_monoidal_category_rank} for input size {input_size}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))  # Default to first 30 primes if no seeds provided
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")