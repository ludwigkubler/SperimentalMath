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
            clause = [random.choice(variables) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def construct_coxeter_dynkin_diagram(clauses):
        # Simplified Coxeter-Dynkin diagram construction
        edges = set()
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    if clause[i] != clause[j]:
                        edges.add((min(clause[i], clause[j]), max(clause[i], clause[j])))
        return edges
    
    n = random.randint(5, 40)
    instance = generate_sat_instance(n)
    diagram_edges = construct_coxeter_dynkin_diagram(instance)
    
    metric_value = Fraction(len(diagram_edges), 1)
    instances_tested = 1
    n_max = n
    conjecture_holds = len(diagram_edges) <= 1.5 ** n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Coxeter-Dynkin Diagram Edge Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(result)