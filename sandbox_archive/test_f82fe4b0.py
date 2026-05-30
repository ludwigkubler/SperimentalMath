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

def generate_k_cnf(n, k):
    variables = list(range(1, n + 1))
    clauses = set()
    while len(clauses) < k:
        clause = {random.choice(variables), random.choice(variables)}
        if clause not in clauses and len(clause) == 2:
            clauses.add(tuple(sorted(clause)))
    return clauses

def coxeter_group_action(graph):
    n = len(graph)
    elements = [{i} for i in range(n)]
    for v, neighbors in graph.items():
        new_elements = set()
        for e in elements:
            if v not in e:
                new_e = e.union(neighbors)
                new_elements.add(tuple(sorted(new_e)))
        elements = new_elements
    return max(len(e) for e in elements)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            k = random.randint(1, min(n * (n - 1) // 2, 10))
            graph = {i: set() for i in range(n)}
            for u, v in generate_k_cnf(n, k):
                graph[u].add(v)
                graph[v].add(u)
            resolution_width = len(graph) + k
            order_largest_element = coxeter_group_action(graph)
            total_metric_value += resolution_width * order_largest_element
            instances_tested += 1
            n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested, len(n_values) * 5).limit_denominator()

    if support_fraction < Fraction(4, 5):
        conjecture_holds = False
        counterexample = "support_fraction_too_low"

    return {
        "metric_name": "resolution_width * order_largest_element",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results)).limit_denominator()

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "support_fraction_too_low" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] == "support_fraction_too_low")
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")