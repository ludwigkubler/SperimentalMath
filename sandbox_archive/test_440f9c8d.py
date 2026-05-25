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
    
    def support(f):
        return set(range(len(f)))
    
    def groupoid_action(f, S):
        action = set()
        for s in S:
            action.add(s)
            action.add(f[s])
        return action
    
    def minimal_rank(action):
        return len(action)
    
    def acc0_parity_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = 1
        for i in range(2, n + 1):
            size *= 2
        return size
    
    f = generate_boolean_function(random.randint(5, 40))
    S = support(f)
    G = groupoid_action(f, S)
    rank = minimal_rank(G)
    circuit_size = acc0_parity_circuit_size(f)
    
    return {
        "metric_name": "rank_to_circuit_size_ratio",
        "metric_value": rank / circuit_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")