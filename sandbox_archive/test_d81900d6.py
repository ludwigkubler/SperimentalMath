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
    
    def count_monomial_symmetries(f):
        n = int(math.log2(len(f)))
        symmetries = set()
        for i in range(2**n):
            permuted = [f[(i >> j) & 1] for j in range(n-1, -1, -1)]
            if f == permuted:
                symmetries.add(tuple(permuted))
        return len(symmetries)
    
    def compute_minimal_local_defect_complexity(f):
        n = int(math.log2(len(f)))
        defect_count = 0
        for i in range(2**n):
            for j in range(n):
                if f[i] != f[(i ^ (1 << j))]:
                    defect_count += 1
        return defect_count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = generate_boolean_function(n)
            D_f = compute_minimal_local_defect_complexity(f)
            S_f = count_monomial_symmetries(f)
            results.append((D_f, S_f))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [D / S for D, S in results if S > 0]
    mean_ratio = sum(ratios) / len(ratios)
    support_fraction = len([r for r in ratios if r <= 1]) / len(ratios)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else "support_fraction < 0.9"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] and r["instances_tested"] >= 30 for r in results):
        RESULT = "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results)) if len(results) > 1 else 'N/A'} support_fraction={'{:.2f}'.format(sum(1 for r in results if r['conjecture_holds']) / len(results))}")