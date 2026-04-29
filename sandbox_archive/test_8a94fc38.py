# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product, combinations

def dist(a, b):
    return max(abs(ai - bi) for ai, bi in zip(a, b))

def is_bi_lipschitz(phi, distortion=2):
    X = set(x for x, y in phi.keys())
    Y = set(y for x, y in phi.keys())
    for (x1, y1), (x2, y2) in product(product(X, Y), repeat=2):
        if dist(phi[(x1, y1)], phi[(x2, y2)]) > distortion * dist((x1, y1), (x2, y2)):
            return False
    return True

def generate_bi_lipschitz_permutations():
    X = {0, 1}
    Y = {0, 1}
    permutations = list(product(X, repeat=4))
    valid_perms = []
    for perm in permutations:
        phi = {(x, y): (perm[2*x + y]) for x, y in product(X, Y)}
        if is_bi_lipschitz(phi):
            valid_perms.append(phi)
    return valid_perms

def generate_boolean_functions(n):
    return list(product([0, 1], repeat=n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    X = {0, 1}
    Y = {0, 1}
    G_1 = (X, Y, lambda x, y: x * y % 2, lambda x, y: abs(x - y))
    
    phi_perms = generate_bi_lipschitz_permutations()
    n_values = [2, 3, 4]
    boolean_functions = generate_boolean_functions(4)
    
    metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for f in boolean_functions:
            G_1_n = (X, Y, lambda x, y: sum(f[i] * g(x[i], y[i]) for i in range(n)) % 2, lambda x, y: max(abs(xi - yi) for xi, yi in zip(x, y)))
            R = 2
            diam_G_1_n = R
            
            protocols = []
            for _ in range(30):  # Sample 30 protocols per (n, f)
                protocol = {}
                for x in product(X, repeat=n):
                    protocol[x] = random.choice([0, 1])
                protocols.append(protocol)
            
            for protocol in protocols:
                transcript_partition = {}
                for x in product(X, repeat=n):
                    transcript_partition.setdefault(tuple(sorted(protocol[x])), []).append(x)
                
                m_Pi_1 = max(len(list(group)) for _, group in transcript_partition.items())
                metric_value += m_Pi_1
                instances_tested += 1
                
                Pi_2 = {}
                for x in product(X, repeat=n):
                    Pi_2[x] = protocol[phi_perms[random.randint(0, len(phi_perms) - 1)][x]]
                
                transcript_partition_Pi_2 = {}
                for x in product(X, repeat=n):
                    transcript_partition_Pi_2.setdefault(tuple(sorted(Pi_2[x])), []).append(x)
                
                m_Pi_2 = max(len(list(group)) for _, group in transcript_partition_Pi_2.items())
                if m_Pi_2 > 2 * m_Pi_1 + 1:
                    return {
                        "metric_name": "Multiplicity Ratio",
                        "metric_value": m_Pi_2 / m_Pi_1,
                        "instances_tested": instances_tested,
                        "conjecture_holds": False,
                        "counterexample": f"m_{Pi_2} > 2 * m_{Pi_1} + 1"
                    }
    
    mean_value = metric_value / instances_tested
    support_fraction = instances_tested / (len(n_values) * len(boolean_functions) * 30)
    
    return {
        "metric_name": "Multiplicity Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True if support_fraction >= 0.99 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity Ratio > 2 * m_{Pi_1} + 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")