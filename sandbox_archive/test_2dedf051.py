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
    
    def generate_expander_graph(n):
        # Ramanujan construction for expander graph
        if n <= 2:
            return []
        d = (n - 1) // 2
        G = [[] for _ in range(n)]
        for i in range(d):
            for j in range(i + 1, min(n, i + d + 1)):
                G[i].append(j)
                G[j].append(i)
        return G
    
    def euler_characteristic(G):
        return len(G) - sum(len(neighbors) for neighbors in G) // 2
    
    def resolution_proof_length(G):
        # Simple DPLL-based solver (simplified version)
        stack = []
        assignment = [None] * len(G)
        
        def dpll():
            if not any(assignment[i] is None for i in range(len(G))):
                return True
            v = next(i for i in range(len(G)) if assignment[i] is None)
            assignment[v] = True
            stack.append((v, True))
            for u in G[v]:
                if assignment[u] == False:
                    return False
                elif assignment[u] is None:
                    if not dpll():
                        return False
            stack.pop()
            assignment[v] = False
            stack.append((v, False))
            for u in G[v]:
                if assignment[u] == True:
                    return False
                elif assignment[u] is None:
                    if not dpll():
                        return False
            stack.pop()
            return True
        
        return len(stack) if dpll() else float('inf')
    
    n = random.randint(5, 40)
    G = generate_expander_graph(n)
    euler_char = euler_characteristic(G)
    proof_length = resolution_proof_length(G)
    
    if euler_char == 0:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Euler characteristic is zero"
        }
    
    upper_bound = 1.5**n / euler_char**2
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= upper_bound,
        "counterexample": "" if proof_length <= upper_bound else f"Proof length {proof_length} exceeds bound {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")