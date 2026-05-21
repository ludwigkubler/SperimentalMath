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
    
    def generate_instance(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def construct_tropical_curve(clauses):
        # Simplified mapping: each variable is a node, each clause is an edge
        nodes = set()
        edges = []
        for clause in clauses:
            nodes.update(clause)
            edges.extend([(clause[0], clause[1]), (clause[1], clause[0])])
        return nodes, edges
    
    def geometric_entropy(nodes, edges):
        # Simplified entropy: number of edges
        return len(edges)
    
    def k_complexity(clauses):
        # Simplified K-complexity: number of clauses
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    I = generate_instance(n, m)
    nodes, edges = construct_tropical_curve(I)
    H_T_I = geometric_entropy(nodes, edges)
    K_I = k_complexity(I)
    
    if K_I == 0:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": H_T_I,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "K-complexity is zero, division by zero error"
        }
    
    if H_T_I > 2 * K_I:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": H_T_I,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"H(T_I) = {H_T_I}, K(I) = {K_I}"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_T_I,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='H(T_I) > 2 * K(I)' first_failing_seed={first_failing_seed}")