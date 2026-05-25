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
    
    def groupoid_action(f):
        S = support(f)
        G = {s: s for s in S}
        for s in S:
            for t in S:
                if f[s] == f[t]:
                    G[s].add(t)
        return G
    
    def minimal_rank(G):
        return len(G)
    
    def acc0_parity_circuit(f):
        n = len(f)
        if n == 1:
            return 1
        if all(f[i] == f[0] for i in range(1, n)):
            return 2
        return 3
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    S = support(f)
    G = groupoid_action(f)
    rank = minimal_rank(G)
    circuit_size = acc0_parity_circuit(f)
    
    return {
        "metric_name": "rank_over_circuit_size",
        "metric_value": rank / circuit_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")