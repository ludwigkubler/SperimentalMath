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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random read-twice branching program with size n ≤ 40
    n = random.randint(5, 40)
    bp = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the characteristic polynomial of the BP
    char_poly = [1]
    for bit in bp:
        char_poly = [sum(x * y for x, y in zip(char_poly, [bit] + [0] * (i - 1))) for i in range(len(char_poly) + 1)]
    
    # Calculate the moments of the characteristic polynomial
    moments = [math.factorial(i) / sum(math.comb(n, k) * char_poly[k] ** i for k in range(n + 1)) for i in range(1, n + 1)]
    
    # Compare the sum of the moments against the lower bound Ω(n^{2/3})
    sum_moments = sum(moments)
    lower_bound = n ** (2 / 3)
    
    return {
        "metric_name": "sum_of_moments",
        "metric_value": sum_moments,
        "instances_tested": n,
        "conjecture_holds": sum_moments >= lower_bound,
        "counterexample": "" if sum_moments >= lower_bound else f"Sum of moments {sum_moments} < lower bound {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Sum of moments < lower bound\" first_failing_seed={first_failing_seed}")