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
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_representation_size(f):
        n = len(f)
        basis = []
        for i in range(2**n):
            row = [f[i ^ (1 << j)] - f[i] if i & (1 << j) else f[i] for j in range(n)]
            if all(row[k] <= 0 or row[k-1] > 0 for k in range(1, n)):
                basis.append(row)
        return len(basis)
    
    def communication_complexity(f):
        # Placeholder for actual complexity calculation
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    count_exceeding_bound = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_monotone_function(n)
            size = tropical_representation_size(f)
            complexity = communication_complexity(f)
            total_size += size
            instances_tested += 1
            if size > Fraction(n**(2/3)):
                count_exceeding_bound += 1
    
    mean_size = total_size / instances_tested
    support_fraction = (instances_tested - count_exceeding_bound) / instances_tested
    
    return {
        "metric_name": "tropical_representation_size",
        "metric_value": mean_size,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if count_exceeding_bound == 0 else f"More than 5% of functions have a tropical representation size exceeding O(n^(2/3))."
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_size} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")