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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_monotonic(f):
        n = len(f)
        for i in range(1 << n):
            if any(f[i | (1 << j)] < f[i] for j in range(n)):
                return False
        return True
    
    def generate_boolean_function(degree):
        return [random.choice([0, 1]) for _ in range(1 << degree)]
    
    def coxeter_dynkin_diagram(f):
        n = len(f)
        diagram = {}
        for i in range(1 << n):
            for j in range(n):
                if f[i | (1 << j)] > f[i]:
                    diagram[(i, i | (1 << j))] = 1
        return diagram
    
    def count_symmetry_classes(diagram):
        visited = set()
        classes = 0
        for node in diagram:
            if node not in visited:
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current not in visited:
                        visited.add(current)
                        for neighbor in diagram:
                            if diagram.get((current, neighbor), 0) == diagram.get((neighbor, current), 0):
                                queue.append(neighbor)
                classes += 1
        return classes
    
    def polynomial_bound(degree):
        # Placeholder for a polynomial bound function
        # This is just an example; replace with actual logic
        return degree**2 + 3*degree + 5
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    if not is_monotonic(f):
        return {
            "metric_name": "symmetry_classes",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "function_not_monotonic"
        }
    
    diagram = coxeter_dynkin_diagram(f)
    symmetry_classes = count_symmetry_classes(diagram)
    bound = polynomial_bound(n)
    
    return {
        "metric_name": "symmetry_classes",
        "metric_value": symmetry_classes,
        "instances_tested": 1,
        "conjecture_holds": symmetry_classes <= bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"function_not_monotonic\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")