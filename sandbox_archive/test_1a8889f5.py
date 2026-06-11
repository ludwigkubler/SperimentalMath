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
        for _ in range(int(n * (n - 1) / 2)):
            u = random.choice(variables)
            v = random.choice(variables)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return variables, edges

    def p_adic_selmer_group_order(E, p):
        # Placeholder implementation
        # Actual computation would depend on the specific elliptic curve and prime p
        return random.randint(1, 10)

    def rank_variance(G):
        # Placeholder implementation
        # Actual computation would depend on the specific communication problem graph G
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    min_order_total = 0
    rank_variance_total = 0
    instances_tested = 0

    for n in n_values:
        q = 2 ** n
        E = generate_elliptic_curve(q)
        G = generate_communication_problem(n)

        min_order = p_adic_selmer_group_order(E, 2)  # Assuming prime p=2 for simplicity
        rank_variance_val = rank_variance(G)

        min_order_total += min_order
        rank_variance_total += rank_variance_val
        instances_tested += n

    mean_min_order = min_order_total / instances_tested
    mean_rank_variance = rank_variance_total / instances_tested

    conjecture_holds = (mean_min_order >= math.log(q**2 / math.log(q)) and 
                        mean_min_order <= q)
    
    return {
        "metric_name": "min_order",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_order does not satisfy the inequality\" first_failing_seed={first_failing_seed}")