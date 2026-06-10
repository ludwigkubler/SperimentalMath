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
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = sum(1 for i in range(1, 2**n) if all(f[i ^ j] == f[j] for j in range(i)))
        return rank / (2**(n-1) - 1)
    
    def monomial_ideal(f):
        n = int(math.log2(len(f)))
        ideal = set()
        for i in range(1, 2**n):
            if all(f[i ^ j] == f[j] for j in range(i)):
                ideal.add(tuple(sorted([j for j in range(n) if (i >> j) & 1])))
        return ideal
    
    def minimal_generators(ideal):
        generators = list(ideal)
        while True:
            new_generators = set()
            for g in generators:
                new_g = tuple(sorted(set(g) | {h} for h in generators if any(j in g for j in h)))
                if new_g not in ideal:
                    new_generators.add(new_g)
            if not new_generators:
                break
            generators.extend(new_generators)
        return len(generators)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    R_f = communication_complexity_rank_variance(f)
    G = monomial_ideal(f)
    m_G = minimal_generators(G)
    
    return {
        "metric_name": "minimal_generators",
        "metric_value": m_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_G <= 0.3 * R_f**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")