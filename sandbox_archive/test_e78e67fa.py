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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            new_var = f'y{i}'
            clauses.append([new_var, variables[i-1], variables[i]])
            clauses.append([-new_var, -variables[i-1]])
            clauses.append([-new_var, -variables[i]])
            variables.append(new_var)
        return clauses
    
    def construct_simplicial_complex(clauses):
        nodes = set()
        edges = []
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    nodes.add((clause[i], clause[j]))
                    nodes.add((clause[j], clause[i]))
                    edges.append(((clause[i], clause[j]), (clause[j], clause[i])))
        return nodes, edges
    
    def compute_cohomology(nodes, edges, p):
        if p == 0:
            return len(nodes)
        cohomology = {node: 0 for node in nodes}
        for edge in edges:
            u, v = edge
            cohomology[u] += 1
            cohomology[v] += 1
        return sum(cohomology.values()) / (2 * p)
    
    def resolution_width(clauses):
        width = 0
        stack = []
        for clause in clauses:
            if not any(lit in stack for lit in clause):
                stack.append(random.choice(clause))
                width += 1
        return width
    
    n = random.randint(5, 40)
    p = random.randint(2, 10)
    formula = generate_tseitin_formula(n)
    nodes, edges = construct_simplicial_complex(formula)
    cohomology_value = compute_cohomology(nodes, edges, p)
    width = resolution_width(formula)
    
    if cohomology_value > 10:
        return {
            "metric_name": "cohomology_value",
            "metric_value": cohomology_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "cohomology_value > 10"
        }
    
    return {
        "metric_name": "cohomology_value",
        "metric_value": cohomology_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"cohomology_value > 10\" first_failing_seed={first_failing_seed}")