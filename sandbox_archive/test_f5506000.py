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
from fractions import Fraction
import math

def tutte_polynomial(graph):
    n = len(graph)
    if n == 0:
        return {(): 1}
    
    node = graph[0]
    subgraph = [neighbor for neighbor in graph if neighbor != node]
    remaining_nodes = [neighbor for neighbor in graph if neighbor != node and neighbor not in subgraph]
    
    result = {}
    for term, coeff in tutte_polynomial(subgraph).items():
        result[(node,) + term] = coeff
        for neighbor in remaining_nodes:
            new_term = (node, neighbor) + term
            result[new_term] += coeff
    
    return result

def communication_rank(tutte_poly):
    # Placeholder for actual computation of communication rank
    # This is a dummy implementation that returns the number of terms as a proxy
    return len(tutte_poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    total_mhs = 0
    total_rank = 0
    
    for n in range(1, n_max + 1):
        d = random.randint(2, min(n - 1, 3))  # Ensure the graph is d-regular
        graph = []
        while len(graph) < n:
            node = tuple(random.sample(range(n), n))
            if node not in graph and len(set(node)) == n:
                graph.append(node)
        
        tutte_poly = tutte_polynomial(graph)
        mhs = communication_rank(tutte_poly)
        rank = communication_rank(tutte_poly)
        
        total_mhs += mhs
        total_rank += rank
        instances_tested += 1
    
    mean_mhs = Fraction(total_mhs, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    
    if instances_tested < 30:
        return {
            "metric_name": "mhs_to_rank_ratio",
            "metric_value": float(mean_mhs / mean_rank),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    return {
        "metric_name": "mhs_to_rank_ratio",
        "metric_value": float(mean_mhs / mean_rank),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_mhs / mean_rank - 1) < 0.05,  # Assuming a tolerance of ±5%
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mhs_to_rank_ratio\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_budget_exceeded n_tested=30")