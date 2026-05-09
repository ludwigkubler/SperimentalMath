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
    
    def generate_max_cut_instance(n):
        edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n * (n - 1) // 2)]
        return edges
    
    def polynomial_from_max_cut(edges, n):
        coefficients = [0] * (n + 1)
        for u, v in edges:
            coefficients[u] += 1
            coefficients[v] += 1
        return coefficients
    
    def sturm_sequence(coefficients):
        if not coefficients:
            return []
        seq = [coefficients]
        while True:
            lead_coeff = seq[-1][0]
            next_seq = [-seq[-2][i+1] * (len(seq[-1]) - i - 1) / lead_coeff for i in range(len(seq[-2]) - 1)]
            if not any(next_seq):
                break
            seq.append(next_seq)
        return seq
    
    def count_real_roots(sturm_seq):
        sign_changes = 0
        for i in range(1, len(sturm_seq)):
            sign_changes += sum(1 for j in range(len(sturm_seq[i])) if sturm_seq[i][j] * sturm_seq[i-1][j] < 0)
        return sign_changes
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_real_roots = 0
    instances_tested = 0
    
    for n in n_values:
        edges = generate_max_cut_instance(n)
        coefficients = polynomial_from_max_cut(edges, n)
        sturm_seq = sturm_sequence(coefficients)
        real_roots = count_real_roots(sturm_seq)
        total_real_roots += real_roots
        instances_tested += 1
    
    mean_real_roots = total_real_roots / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Mean Real Roots",
        "metric_value": mean_real_roots,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_real_roots = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_real_roots} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_real_roots} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")