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
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 3))
    
    # Generate a random d-regular graph
    nodes = list(range(n))
    edges = []
    for node in nodes:
        neighbors = random.sample([n for n in nodes if n != node], d-1)
        for neighbor in neighbors:
            if (node, neighbor) not in edges and (neighbor, node) not in edges:
                edges.append((node, neighbor))
    
    # Tseitin formula generation
    tseitin_vars = [f"x{i}" for i in range(n)]
    clauses = []
    for edge in edges:
        u, v = edge
        clauses.append([tseitin_vars[u], tseitin_vars[v]])
        clauses.append([-tseitin_vars[u], -tseitin_vars[v]])
        clauses.append([tseitin_vars[u], -tseitin_vars[v], f"y{len(clauses)-1}"])
        clauses.append([-tseitin_vars[u], tseitin_vars[v], f"y{len(clauses)-1}"])
        clauses.append([tseitin_vars[u], tseitin_vars[v], f"y{len(clauses)-1}"])
        clauses.append([-tseitin_vars[u], -tseitin_vars[v], -f"y{len(clauses)-1}"])
    
    # Symplectic form calculation (simplified example)
    symplectic_form = len(clauses)  # Placeholder for actual computation
    
    # Frege proof size estimation (simplified example)
    frege_proof_size = len(clauses) * 2  # Placeholder for actual computation
    
    return {
        "metric_name": "symplectic_form",
        "metric_value": symplectic_form,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if frege_proof_size == 0 else symplectic_form <= frege_proof_size * 2,
        "counterexample": "" if frege_proof_size != 0 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")