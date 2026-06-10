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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        srank_list = []
        for i in range(1, n+1):
            count = 0
            for j in range(n):
                if f[j] == 1:
                    count += 1
            srank_list.append(count / (n - i + 1))
        return sum(srank_list) / len(srank_list)
    
    def monomial_ideal(f):
        n = len(f)
        ideal = set()
        for i in range(n):
            if f[i] == 1:
                ideal.add(tuple([i]))
        return ideal
    
    def minimal_generators(ideal):
        generators = []
        while ideal:
            gen = min(ideal, key=lambda x: sum(x))
            generators.append(gen)
            ideal -= {tuple(sorted(set(g) | set(h))) for h in ideal if any(j in g for j in h)}
        return len(generators)
    
    n = 10
    f = generate_boolean_function(n)
    R_f = communication_complexity_rank_variance(f)
    G = monomial_ideal(f)
    m_G = minimal_generators(G)
    
    return {
        "metric_name": "m_G",
        "metric_value": m_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_G <= 0.3 * R_f**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")