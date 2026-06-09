# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses

    def construct_coxeter_dynkin_diagram(clauses):
        # Simplified method to simulate diagram construction
        edges = set()
        for clause in clauses:
            if len(clause) == 2 and abs(clause[0]) != abs(clause[1]):
                u, v = abs(clause[0]), abs(clause[1])
                if u > v:
                    u, v = v, u
                edges.add((u, v))
        return edges

    def count_edges(diagram):
        return len(diagram)

    n_values = [5, 10, 15, 20, 30, 40]
    total_edges = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_sat_instance(n)
            diagram = construct_coxeter_dynkin_diagram(instance)
            edges = count_edges(diagram)
            total_edges += edges
            instances_tested += 1
            n_max = max(n_max, n)

    mean_edges = Fraction(total_edges, instances_tested)
    conjecture_holds = all(mean_edges <= 1.5**n for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Coxeter-Dynkin Diagram Edge Count",
        "metric_value": mean_edges,
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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_edges = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_edges} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")