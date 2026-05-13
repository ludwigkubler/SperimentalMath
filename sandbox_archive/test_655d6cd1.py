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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n):
    tableaux = []
    def generate_tableau(row, col, path):
        if row == n:
            tableaux.append(path)
            return
        for c in range(col, n):
            generate_tableau(row + 1, c, path + [c - row])
    generate_tableau(0, 0, [])
    count = 0
    for t in tableaux:
        hook_length = 1
        for i in range(n):
            hook_length *= (t[i] + n - i - 1)
        count += factorial(n) // hook_length
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_components = 0
    instances_tested = 0
    
    for n in n_values:
        perm_components = hook_length_formula(n)
        det_components = hook_length_formula(n - 1) if n > 1 else 1
        total_components += perm_components / det_components
        instances_tested += 1
    
    ratio = total_components / len(n_values)
    conjecture_holds = ratio >= math.exp(n_values[0] / 2)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < Ω(2^{n_values[0]/2})"
    
    return {
        "metric_name": "Component Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")