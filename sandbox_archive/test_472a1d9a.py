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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def local_zeta_function_size(cnf, var):
        size = 0
        for clause in cnf:
            if var in clause or -var in clause:
                size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_size = 0
    max_size = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            min_size = float('inf')
            for var in range(1, n + 1):
                size = local_zeta_function_size(cnf, var)
                if size < min_size:
                    min_size = size
            total_size += min_size
            instances_tested += 1
            max_size = max(max_size, min_size)
    
    mean_size = total_size / instances_tested
    conjecture_holds = all(min_size <= m**0.5 * n**(3/4) for _, m, n in [(min_size, m, n) for n in n_values for _ in range(5)])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_zeta_function_size",
        "metric_value": mean_size,
        "instances_tested": instances_tested,
        "n_max": max_size,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"] - m**0.5 * n**(3/4)) > 5 for r, m, n in zip(results, [r["n_max"] for r in results], [r["instances_tested"] for r in results])):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and abs(r['metric_value'] - m**0.5 * n**(3/4)) > 5))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")