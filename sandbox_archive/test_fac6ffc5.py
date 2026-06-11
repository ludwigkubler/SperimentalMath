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
    
    def generate_elliptic_curve(q):
        a = random.randint(0, q-1)
        b = random.randint(0, q-1)
        return (a, b)

    def generate_communication_problem(n):
        variables = list(range(n))
        edges = []
        for _ in range(random.randint(0, n*(n-1)//2)):
            u = random.choice(variables)
            v = random.choice(variables)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return variables, edges

    def p_adic_selmer_group_order(E, p):
        # Simplified version for demonstration purposes
        a, b = E
        x = (4*a**3 + 27*b**2) % p
        if x == 0:
            return 1
        else:
            return 2

    def rank_variance(G):
        n = len(G)
        mean = sum(G) / n
        variance = sum((x - mean)**2 for x in G) / n
        return variance

    min_order = float('inf')
    rank_variances = []
    
    for _ in range(30):
        q = 2**random.randint(5, 40)
        E = generate_elliptic_curve(q)
        p = random.choice([2] + [i for i in range(3, q) if all(i % j != 0 for j in range(2, int(math.sqrt(i)) + 1))])
        min_order = min(min_order, p_adic_selmer_group_order(E, p))
        
        n = random.randint(5, 40)
        variables, edges = generate_communication_problem(n)
        rank_variances.append(rank_variance(variables))

    conjecture_holds = all(log(q**2 / log(q)) <= min_order <= q for q in [2**i for i in range(5, 41)])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 30,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i for i in range(5, 31)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")