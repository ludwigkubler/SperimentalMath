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
    
    n = 40
    instances_tested = 30
    
    # Generate random unit vectors
    vectors = []
    for _ in range(instances_tested):
        vector = [random.gauss(0, 1) for _ in range(n)]
        norm = math.sqrt(sum(x**2 for x in vector))
        vectors.append([x / norm for x in vector])
    
    # Compute the inner products
    inner_products = []
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            inner_product = sum(vectors[i][k] * vectors[j][k] for k in range(n))
            inner_products.append(inner_product)
    
    # Estimate the discrepancy
    mean_discrepancy = abs(sum(inner_products) / len(inner_products))
    lower_bound = math.sqrt(math.log(n))
    
    conjecture_holds = mean_discrepancy >= lower_bound
    counterexample = f"mean_discrepancy={mean_discrepancy}, lower_bound={lower_bound}" if not conjecture_holds else ""
    
    return {
        "metric_name": "discrepancy",
        "metric_value": mean_discrepancy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_discrepancy = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_discrepancy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")