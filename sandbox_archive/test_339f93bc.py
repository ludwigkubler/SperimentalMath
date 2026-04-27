# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gray_code(n):
    if n == 0:
        return ['']
    half = gray_code(n - 1)
    return ['0' + x for x in half] + ['1' + x for x in reversed(half)]

def truth_table(f, n):
    inputs = [i for i in range(2**n)]
    outputs = [f(i) for i in inputs]
    return outputs

def p_w(k, w):
    factors = set()
    for i in range(len(w) - k + 1):
        factor = tuple(w[i:i+k])
        factors.add(factor)
    return len(factors)

def dnf_min(f, n):
    tt = truth_table(f, n)
    prime_implicants = []
    for i in range(2**n):
        if tt[i] == 1:
            pi = [i]
            for j in range(i + 1, 2**n):
                if tt[j] == 1 and all((j & (1 << k)) == (i & (1 << k)) for k in range(n)):
                    pi.append(j)
            prime_implicants.append(pi)
    dnf = []
    while prime_implicants:
        min_pi = min(prime_implicants, key=len)
        dnf.append(min_pi)
        prime_implicants = [pi for pi in prime_implicants if not any(pi[i] in min_pi for i in range(len(pi)))]
    return len(dnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    results = []
    
    for n in n_values:
        if n <= 4:
            functions = [(lambda f: f(x)) for x in range(2**n)]
        else:
            functions = random.sample([(lambda f: f(x)) for x in range(2**n)], 5000)
        
        for f in functions:
            w = gray_code(n)
            p_values = [p_w(k, w) / k if k > 0 else 1 for k in range(1, n + 1)]
            P_f = max(p_values)
            DNF_min_f = dnf_min(f, n)
            results.append((P_f, DNF_min_f))
    
    metric_value = sum(DNF_min for _, DNF_min in results) / len(results)
    support_fraction = sum(1 for _, DNF_min in results if DNF_min >= math.ceil(P_f / 2)) / len(results)
    conjecture_holds = support_fraction == 1.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DNF_min vs P(f)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
    
    results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            trial_result = json.load(f)
            results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x >= math.ceil(P_f / 2)) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(x < math.ceil(P_f / 2) for x in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")