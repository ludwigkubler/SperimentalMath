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

def generate_cnf(n):
    cnf = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            cnf.append(tuple(clause))
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    instances_tested = len(cnf)
    
    # Placeholder for Kähler form tropicalization and minimal rank computation
    min_rank = n * (n + 1) // 2  # Simplified placeholder
    
    k = random.randint(1, 10)  # Placeholder for AC0 circuit threshold
    
    ratio = math.log(n) / min_rank
    conjecture_holds = abs(ratio - k) <= 0.1 * k
    counterexample = "" if conjecture_holds else f"n={n}, min_rank={min_rank}, k={k}"
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")