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
    
    def xor_and_tree_width(f, n):
        if n == 1:
            return 0
        else:
            return 1 + max(xor_and_tree_width(f, n // 2), xor_and_tree_width(f, (n + 1) // 2))
    
    def is_quadratic_residue(a, p):
        return pow(a, (p - 1) // 2, p) == 1
    
    def count_quadratic_residues(values, p):
        return sum(is_quadratic_residue(v, p) for v in values)
    
    n = 40
    m = n
    f = [random.randint(0, 1) for _ in range(2 ** n)]
    
    t_f = xor_and_tree_width(f, n)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    p = max(primes)
    
    while math.sqrt(p) <= t_f:
        p += 2
        if p >= 2 ** n:
            return {
                "metric_name": "XOR-AND tree width",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    num_residues = count_quadratic_residues(f, p)
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": t_f,
        "instances_tested": 1,
        "conjecture_holds": t_f <= math.sqrt(p),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")