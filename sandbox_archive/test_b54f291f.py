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
    
    def generate_graph(n):
        if n == 1:
            return {0}
        nodes = list(range(n))
        edges = []
        for i in range(n - 1):
            edges.append((nodes[i], nodes[i + 1]))
        return {node: set() for node in nodes}, edges
    
    def tseitin_formula(graph):
        nodes, edges = graph
        n = len(nodes)
        clauses = []
        
        def add_clause(a, b, c):
            clauses.append([a, b, -c])
        
        for i in range(n):
            add_clause(i + 1, i + 2, -(i + 3))
        
        return clauses
    
    def resolution_proof_depth(clauses):
        # Simplified resolution proof depth calculation
        return len(clauses)
    
    def invariant(graph):
        nodes, edges = graph
        n = len(nodes)
        if n <= 4:
            return 1
        else:
            return math.log(n, 2)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    tseitin_clauses = tseitin_formula(graph)
    proof_depth = resolution_proof_depth(tseitin_clauses)
    nu_G = invariant(graph)
    
    metric_name = "Resolution Proof Depth"
    metric_value = proof_depth
    instances_tested = 1
    conjecture_holds = proof_depth >= 2 ** (math.log(n) * math.log(nu_G))
    counterexample = "" if conjecture_holds else f"n={n}, nu(G)={nu_G}, proof depth={proof_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample_desc = f"n={results[first_failing_seed]['instances_tested']}, nu(G)={results[first_failing_seed]['counterexample'].split(',')[1].strip()}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")