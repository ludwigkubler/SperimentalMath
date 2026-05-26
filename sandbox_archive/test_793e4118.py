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
    
    def generate_tseitin_circuit(n, m):
        inputs = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            a, b, c = random.sample(inputs, 3)
            clause = f"{a} | {b} & ~{c}"
            clauses.append(clause)
        return inputs, clauses
    
    def galois_representation(circuit):
        # Simplified mapping to a permutation group
        n = len(circuit[0])
        G = []
        for i in range(1 << n):
            perm = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    perm[j] = (j + 1) % n + 1
                else:
                    perm[j] = j + 1
            G.append(perm)
        return G
    
    def minimal_order(G):
        p = 2
        while True:
            found = False
            for g in G:
                if all((g[i] - 1) % p == (i - 1) % p for i in range(len(g))):
                    found = True
                    break
            if found:
                return p
            p += 1
    
    n = 5
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        inputs, clauses = generate_tseitin_circuit(n, m)
        G = galois_representation((inputs, clauses))
        order = minimal_order(G)
        results.append(order)
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = all(abs(x - m ** 0.5) <= 0.2 * m ** 0.5 for x, m in zip(results, m_values))
    
    return {
        "metric_name": "min_galois_order",
        "metric_value": mean_value,
        "instances_tested": len(m_values),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mean deviation > 20%"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction=1.0")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mean deviation > 20%' first_failing_seed={first_failing_seed}")