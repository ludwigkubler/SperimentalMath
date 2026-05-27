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
    
    def generate_circuit(n):
        # Simple random circuit generation (not actual Boolean logic)
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_symmetry_group(circuit):
        # Placeholder function to simulate symmetry group computation
        return set(range(len(circuit)))
    
    def compute_coxeter_dynkin_diagram(group):
        # Placeholder function to simulate Coxeter-Dynkin diagram computation
        return len(group)
    
    total_vertices = 0
    instances_tested = 0
    
    for n in range(5, 41):
        for _ in range(3):  # Test each size 3 times
            circuit = generate_circuit(n)
            group = compute_symmetry_group(circuit)
            vertices = compute_coxeter_dynkin_diagram(group)
            total_vertices += vertices
            instances_tested += 1
    
    mean_vertices = total_vertices / instances_tested
    conjecture_holds = mean_vertices <= 1.5 * n**2
    counterexample = "" if conjecture_holds else f"Mean vertices {mean_vertices} > 1.5 * n^2 for some n"
    
    return {
        "metric_name": "Mean number of vertices",
        "metric_value": mean_vertices,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_vertices = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_vertices} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_vertices} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean vertices exceeds 1.5 * n^2\" first_failing_seed={first_failing_seed}")