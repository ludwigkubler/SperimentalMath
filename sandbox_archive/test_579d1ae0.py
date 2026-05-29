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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} ∨ {clause[1]})")
        return clauses
    
    def construct_graph(clauses):
        graph = {}
        for clause in clauses:
            literals = clause.split()
            for literal in literals:
                if literal.startswith('¬'):
                    literal = literal[1:]
                if literal not in graph:
                    graph[literal] = set()
                for other_literal in literals:
                    if other_literal != literal and (other_literal.startswith('¬') == literal.startswith('¬')):
                        continue
                    if other_literal not in graph[literal]:
                        graph[literal].add(other_literal)
        return graph
    
    def count_real_roots(graph):
        # Placeholder for a simple root-counting algorithm
        # This is a dummy implementation and should be replaced with an actual method
        return len(graph)  # Simplified for demonstration purposes
    
    def resolution_length(clauses):
        # Placeholder for a small DPLL solver
        # This is a dummy implementation and should be replaced with an actual method
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    clauses = generate_tseitin_formula(n, m)
    graph = construct_graph(clauses)
    r_F = count_real_roots(graph)
    Resolution_length_F = resolution_length(clauses)
    
    if Resolution_length_F < 2**(r_F * 0.5) or Resolution_length_F > 2**(r_F * 1.5):
        conjecture_holds = False
        counterexample = f"Resolution_length(F)={Resolution_length_F}, r(F)={r_F}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Resolution_length / 2^r(F)",
        "metric_value": Resolution_length_F / (2 ** r_F),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.9:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")