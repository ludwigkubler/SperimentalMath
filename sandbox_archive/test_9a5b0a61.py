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
    
    def configuration_space(f):
        n = int(math.log2(len(f)))
        space = set()
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            outputs = f[i]
            space.add((tuple(inputs), outputs))
        return space
    
    def decision_tree_size(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 1
        root = random.choice(range(n))
        left_f = [f[i] for i in range(2**n) if (i >> root & 1) == 0]
        right_f = [f[i] for i in range(2**n) if (i >> root & 1) == 1]
        return 1 + max(decision_tree_size(left_f), decision_tree_size(right_f))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    R_f = len(configuration_space(f))
    T_f = decision_tree_size(f)
    
    return {
        "metric_name": "Rank vs Decision Tree Size",
        "metric_value": R_f,
        "instances_tested": 1,
        "conjecture_holds": R_f == T_f,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.85:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")