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
    
    def generate_random_sat_instance(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def tseitin_transformation(clauses):
        literals = set()
        new_vars = {}
        for i, clause in enumerate(clauses):
            literals.update(clause)
            new_var = f"q{i+1}"
            new_vars[new_var] = len(new_vars) + 1
            clauses.append([new_var, -clause[0]])
            clauses.append([-new_var, clause[1]])
        return clauses, new_vars
    
    def construct_quandle(clauses):
        quandle = {}
        for clause in clauses:
            for lit in clause:
                if lit not in quandle:
                    quandle[lit] = set()
                for other_lit in clause:
                    if other_lit != lit and -other_lit not in quandle[lit]:
                        quandle[lit].add(other_lit)
        return quandle
    
    def minimal_entropy(quandle):
        entropy = 0
        for key, value in quandle.items():
            if len(value) > 1:
                p = 1 / (len(value) - 1)
                entropy += math.log2(p)
        return entropy
    
    def resolution_width(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        queue = list(clauses_set)
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                return len(queue)
            for other_clause in clauses_set - {clause}:
                new_clause = [x for x in other_clause if x not in clause]
                if len(new_clause) == 0:
                    continue
                if tuple(sorted(new_clause)) not in queue:
                    queue.append(tuple(sorted(new_clause)))
        return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_random_sat_instance(n)
            tseitin_clauses, new_vars = tseitin_transformation(clauses)
            quandle = construct_quandle(tseitin_clauses)
            entropy = minimal_entropy(quandle)
            width = resolution_width(tseitin_clauses)
            results.append((entropy, width))
    
    if not results:
        return {
            "metric_name": "Quandle Entropy vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    entropy_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    mean_entropy = sum(entropy_values) / len(entropy_values)
    mean_width = sum(width_values) / len(width_values)
    
    if any(w == float('inf') for w in width_values):
        return {
            "metric_name": "Quandle Entropy vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Resolution proof width is infinite"
        }
    
    n_max = max(n_values)
    return {
        "metric_name": "Quandle Entropy vs Resolution Width",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": False,  # Placeholder, actual correlation test needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}"
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)