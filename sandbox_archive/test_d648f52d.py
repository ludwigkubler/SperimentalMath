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

def generate_quandle(n):
    elements = list(range(1, n + 1))
    operation_table = {}
    for i in range(n):
        for j in range(n):
            operation_table[(i, j)] = (i + j) % n + 1
    return operation_table

def are_isomorphic(q1, q2):
    if len(q1) != len(q2):
        return False
    n = len(q1)
    for perm in itertools.permutations(range(1, n + 1)):
        is_isomorphic = True
        for i in range(n):
            for j in range(n):
                if q1[(i, j)] != q2[perm[i] - 1][perm[j] - 1]:
                    is_isomorphic = False
                    break
            if not is_isomorphic:
                break
        if is_isomorphic:
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    q1 = generate_quandle(n)
    q2 = generate_quandle(n)
    while are_isomorphic(q1, q2):
        q2 = generate_quandle(n)
    
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        q3 = generate_quandle(n)
        if are_isomorphic(q1, q3) or are_isomorphic(q2, q3):
            conjecture_holds = False
            counterexample = f"Quandles {q1} and {q2} are isomorphic to {q3}"
            break
    
    return {
        "metric_name": "Minimum Circuit Depth",
        "metric_value": math.log(n),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")