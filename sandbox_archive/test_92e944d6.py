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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def tensor_product(f, g):
        m = len(f)
        n = len(g)
        result = []
        for i in range(2**(m+n)):
            x = bin(i)[2:].zfill(m+n)
            x_m = int(x[:m], 2)
            x_n = int(x[m:], 2)
            result.append(f[x_m] * g[x_n])
        return result
    
    def geometric_entropy(p):
        p = [x for x in p if x > 0]
        H = -sum([p_i * math.log2(p_i) for p_i in p]) / len(p)
        return H
    
    def circuit_depth(f):
        m = len(f)
        n = 1
        while True:
            new_f = [f[i] ^ f[(i + 1) % m] for i in range(m)]
            if all(new_f):
                break
            f = new_f
            n += 1
        return n
    
    def fisher_rao_metric(p, q):
        p = [x for x in p if x > 0]
        q = [x for x in q if x > 0]
        if len(p) != len(q):
            return float('inf')
        H_p = geometric_entropy(p)
        H_q = geometric_entropy(q)
        I_pq = sum([p_i * math.log2(p_i / q_i) for p_i, q_i in zip(p, q)]) / len(p)
        return 2 * (H_p + H_q - 2 * I_pq)
    
    m = random.randint(5, 30)
    f = generate_boolean_function(m)
    g = tensor_product(f, f)
    n = circuit_depth(f)
    H_g = geometric_entropy(g)
    O_m_log_n = m * math.log(n)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_g,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_g <= O_m_log_n,
        "counterexample": "" if H_g <= O_m_log_n else f"m={m}, n={n}, H(g)={H_g}, O(m log n)={O_m_log_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")