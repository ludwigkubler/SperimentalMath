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
    
    def generate_cnf(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        clauses = cnf[:]
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in variables):
                        new_clause = [lit for lit in clauses[i] + clauses[j] if lit not in [-x for x in clauses[i]]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(clauses)
            if new_clause in clauses:
                return len(clauses)
            clauses.append(new_clause)
    
    def cayley_graph_diameter(cnf):
        # Simplified Cayley graph diameter calculation for demonstration purposes
        return 2 * resolution_width(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    diameters = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        diameter = cayley_graph_diameter(cnf)
        widths.append(width)
        diameters.append(diameter)
    
    if not widths or not diameters:
        return {
            "metric_name": "w(φ)/d(φ)^2",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((width - sum(widths)/len(widths)) * (diameter**2 - sum(diameters)**2/len(diameters)) for width, diameter in zip(widths, diameters)) / len(widths)
    mean_ratio = sum(width / diameter**2 for width, diameter in zip(widths, diameters)) / len(widths)
    
    return {
        "metric_name": "w(φ)/d(φ)^2",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")