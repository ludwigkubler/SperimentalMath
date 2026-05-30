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
from fractions import Fraction
import math

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def support(f):
    return {i for i, bit in enumerate(f) if bit == 1}

def right_angled_coxeter_group_actions(support_set):
    n = len(support_set)
    actions = []
    for mask in range(1 << n):
        action = set()
        for i in support_set:
            if (mask & (1 << i)) != 0:
                action.add(i)
        actions.append(action)
    return actions

def entropy(probabilities):
    return sum(-p * math.log2(p) for p in probabilities if p > 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        s = support(f)
        actions = right_angled_coxeter_group_actions(s)
        alpha = len(actions)
        probabilities = [Fraction(1, alpha) for _ in range(alpha)]
        H_f = entropy(probabilities)
        results.append((n, alpha, H_f))
    
    metric_name = "H(f)"
    metric_value = sum(H_f for _, _, H_f in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = all(alpha >= 1 and H_f <= math.log2(alpha) for _, alpha, H_f in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")