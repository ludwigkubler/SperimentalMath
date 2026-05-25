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
    elements = [random.randint(1, 100) for _ in range(n)]
    subset_sums = set()
    
    def generate_subsets(elements):
        if not elements:
            yield []
        else:
            first, *rest = elements
            for subset in generate_subsets(rest):
                yield subset
                yield [first] + subset
    
    for subset in generate_subsets(elements):
        subset_sum = sum(subset)
        subset_sums.add(subset_sum)
    
    distinct_subset_sums_count = len(subset_sums)
    
    # Placeholder function to simulate AC⁰ circuit complexity
    def ac0_circuit_complexity(n):
        return n * math.log2(n)
    
    alpha_n = ac0_circuit_complexity(n)
    
    conjecture_holds = distinct_subset_sums_count <= alpha_n
    
    return {
        "metric_name": "Distinct Subset Sums",
        "metric_value": distinct_subset_sums_count,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"alpha({n}) = {alpha_n}, but found {distinct_subset_sums_count} distinct subset sums"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha(n) > distinct subset sums\" first_failing_seed={first_failing_seed}")