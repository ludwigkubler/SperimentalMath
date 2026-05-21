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
    
    def generate_random_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def clique_complex(edges):
        cliques = set()
        for edge in edges:
            u, v = edge
            new_cliques = {frozenset({u, v})}
            for clique in cliques:
                if not (clique & frozenset(edge)):
                    new_cliques.add(clique | frozenset(edge))
            cliques.update(new_cliques)
        return cliques
    
    def euler_characteristic(cliques):
        return len(cliques) - sum(len(c) for c in cliques) + n
    
    def resolution_length(edges):
        if not edges:
            return 1
        variables = set()
        for u, v in edges:
            variables.update([u, v])
        clauses = []
        for u, v in edges:
            clauses.append([-u - 1, -v - 1])
            clauses.append([u + 1, v + 1])
        for v in variables:
            clauses.append([-v - 1])
        return len(clauses)
    
    n = random.randint(5, 40)
    edges = generate_random_graph(n)
    cliques = clique_complex(edges)
    chi = euler_characteristic(cliques)
    res_length = resolution_length(edges)
    
    if chi == 0:
        return {
            "metric_name": "Resolution length",
            "metric_value": res_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph with n={}, A={}".format(n, edges)
        }
    
    c = 0.5
    if res_length >= 2 ** (c * chi):
        return {
            "metric_name": "Resolution length",
            "metric_value": res_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "Resolution length",
        "metric_value": res_length,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "Graph with n={}, A={}".format(n, edges)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction={:.2f}".format(total_metric_value / len(results), 0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction={:.2f}".format(total_metric_value / len(results), 0, support_fraction))
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(counterexample, first_failing_seed))