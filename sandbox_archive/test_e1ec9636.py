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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = []
        for i in range(1, n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if random.choice([True, False]):
                        graph[i].add(j)
                        graph[j].add(i)
                        edges.append((i, j))
        return graph
    
    def frege_proof_depth(graph):
        # Simplified DPLL solver for Frege proof depth
        n = len(graph)
        stack = []
        assignment = [None] * n
        
        def dpll():
            if not stack:
                return True
            v = next(v for v in range(n) if assignment[v] is None)
            for val in [True, False]:
                assignment[v] = val
                new_stack = stack[:]
                for u in graph[v]:
                    if assignment[u] == val:
                        continue
                    if assignment[u] is None:
                        new_stack.append(u)
                    else:
                        return False
                if dpll():
                    return True
            assignment[v] = None
            return False
        
        return 1 + max(dpll() for _ in range(10)) if dpll() else float('inf')
    
    def quantum_affine_generators(graph):
        n = len(graph)
        generators = set()
        for v in graph:
            for u in graph[v]:
                generators.add((v, u))
        return len(generators)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 8))
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        m_G = quantum_affine_generators(graph)
        w_G = frege_proof_depth(graph)
        results.append((m_G, w_G))
    
    if not results:
        return {
            "metric_name": "Frege Proof Depth",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid d-regular graph generated"
        }
    
    m_G_avg = sum(m for m, _ in results) / len(results)
    w_G_avg = sum(w for _, w in results) / len(results)
    n_max = max(n for _, _ in results)
    
    conjecture_holds = all(abs(m - w) <= 0.1 * abs(w) for m, w in results)
    counterexample = "" if conjecture_holds else "Frege Proof Depth does not match Quantum Affine Generators"
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": w_G_avg,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in itertools.product(range(5), range(4), range(3))]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")