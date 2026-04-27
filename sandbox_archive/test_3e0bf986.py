# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import product

def truth_table(f, n):
    inputs = list(product([0, 1], repeat=n))
    outputs = [f(tuple(inputs[i])) for i in range(len(inputs))]
    return outputs

def gray_code(n):
    if n == 0:
        return ['']
    prev_gray = gray_code(n-1)
    return ['0' + code for code in prev_gray] + ['1' + code for code in reversed(prev_gray)]

def factor_complexity(word):
    n = len(word)
    p_w = [0] * (n+1)
    for k in range(1, n+1):
        factors = set()
        for i in range(n-k+1):
            factors.add(word[i:i+k])
        p_w[k] = len(factors)
    return max(p_w) / n

def dnf_min(f, n):
    tt = truth_table(f, n)
    prime_implicants = []
    for i in range(2**n):
        if tt[i]:
            implicant = [i]
            for j in range(i+1, 2**n):
                if (tt[j] and all((j & (1 << k)) == (i & (1 << k)) for k in range(n))):
                    implicant.append(j)
            prime_implicants.append(implicant)
    terms = []
    while prime_implicants:
        selected = None
        for i, imp in enumerate(prime_implicants):
            if not any(all((j & (1 << k)) == (i & (1 << k)) for k in range(n)) for j in imp for other in prime_implicants[i+1:]):
                selected = i
                break
        if selected is None:
            break
        terms.append(prime_implicants[selected])
        prime_implicants = [imp for i, imp in enumerate(prime_implicants) if not any(all((j & (1 << k)) == (i & (1 << k)) for k in range(n)) for j in imp)]
    return len(terms)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        functions = [(lambda f: lambda x: f(x)) for _ in range(2**n)]
        random.shuffle(functions)
        for f in functions[:5000]:
            w_f = ''.join(str(bit) for bit in truth_table(f, n))
            p_w_f = factor_complexity(w_f)
            DNF_min_f = dnf_min(f, n)
            metric_value = DNF_min_f >= math.ceil(p_w_f / 2)
            total_metric_value += int(metric_value)
            instances_tested += 1
            if not metric_value:
                conjecture_holds = False
                counterexample = f"n={n}, function: {f}"

    return {
        "metric_name": "DNF_min >= ceil(P(f)/2)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    total_metric_value = sum(res["metric_value"] * res["instances_tested"] for res in results) / sum(res["instances_tested"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")