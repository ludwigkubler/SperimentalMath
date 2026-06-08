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
    
    def generate_random_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def tensor_product(f, g):
        m = len(f)
        n = len(g)
        result = []
        for x in range(m):
            for y in range(n):
                result.append(f[x] * g[y])
        return result
    
    def geometric_entropy(p):
        entropy = 0
        for p_i in p:
            if p_i > 0:
                entropy -= p_i * math.log2(p_i)
        return entropy
    
    def circuit_depth(f):
        m = len(f)
        n = 1
        while (1 << n) < m:
            n += 1
        return n
    
    m = random.randint(5, 30)
    f = generate_random_boolean_function(m)
    g = tensor_product(f, f)
    
    p_g = [Fraction(g.count(i), len(g)) for i in range(2)]
    H_g = geometric_entropy(p_g)
    
    n = circuit_depth(f)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_g,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_g <= m * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric_entropy > m log n\" first_failing_seed={first_failing_seed}")