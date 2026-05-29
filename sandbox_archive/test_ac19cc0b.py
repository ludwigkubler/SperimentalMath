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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def read_twice_bp_size(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid boolean function length")
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] == f[j]:
                    count += 1
        return count
    
    def br_group_order(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid boolean function length")
        order = 1
        for i in range(n):
            order *= (f[i] + f[(i + 1) % n]) % 2
        return order
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(2, 100) if is_prime(i)]
    
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            rtbp_size = read_twice_bp_size(f)
            for p in primes:
                br_order = br_group_order(f)
                if br_order > rtbp_size:
                    conjecture_holds = False
                    counterexample = f"n={n}, RTBP(f)={rtbp_size}, |Br(G_f)|={br_order}"
                    break
            total_metric_value += br_order / rtbp_size
            instances_tested += 1
    
    return {
        "metric_name": "BR/RTBP ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) > 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")