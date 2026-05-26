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
    
    n = 5  # Fixed number of inputs
    m_min = 10
    m_max = 40
    
    def generate_tseitin_circuit(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        
        for _ in range(m):
            literals = random.sample(variables + [-v for v in variables], 2)
            if literals[0] > 0 and literals[1] > 0:
                clauses.append((literals[0], literals[1]))
            elif literals[0] < 0 and literals[1] < 0:
                clauses.append((-literals[0], -literals[1]))
            else:
                clauses.append((literals[0], -literals[1]))
        
        return variables, clauses
    
    def galois_representation(clauses):
        # Simplified mapping to a group action
        G = set()
        for clause in clauses:
            if len(clause) == 2 and clause[0] > 0 and clause[1] < 0:
                G.add((clause[0], -clause[1]))
        
        return G
    
    def minimal_order(G):
        # Simplified order calculation
        return max(len(g) for g in G)
    
    total_metric = 0
    instances_tested = 0
    
    for m in range(m_min, m_max + 1):
        variables, clauses = generate_tseitin_circuit(n, m)
        G = galois_representation(clauses)
        order = minimal_order(G)
        
        if order == 0:
            continue
        
        total_metric += order
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "minimal_order",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid Galois representation found"
        }
    
    mean_value = total_metric / instances_tested
    std_dev = math.sqrt(sum((order - mean_value) ** 2 for order in range(m_min, m_max + 1)) / instances_tested)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(mean_value - math.sqrt(m_min)) < 0.2 * math.sqrt(m_min),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")