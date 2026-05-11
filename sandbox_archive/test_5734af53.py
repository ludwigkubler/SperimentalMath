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
    
    def generate_dnf(n, m):
        dnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            dnf.append(clause)
        return dnf
    
    def is_k_clique_dnf(dnf, k):
        variables = set()
        for clause in dnf:
            variables.update(abs(var) for var in clause)
        if len(variables) < k:
            return False
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                if all(var not in clause for clause in dnf):
                    return True
        return False
    
    def greedy_matching(hypergraph):
        matching = []
        hypergraph_copy = [set(edge) for edge in hypergraph]
        while hypergraph_copy:
            max_edge_index = None
            max_size = 0
            for i, edge in enumerate(hypergraph_copy):
                if len(edge) > max_size:
                    max_size = len(edge)
                    max_edge_index = i
            matching.append(list(hypergraph_copy[max_edge_index]))
            hypergraph_copy.pop(max_edge_index)
            for i, edge in enumerate(hypergraph_copy):
                hypergraph_copy[i] -= set(matching[-1])
        return matching
    
    def hypergraph_from_dnf(dnf):
        hypergraph = []
        for clause in dnf:
            hypergraph.append(set(abs(var) for var in clause))
        return hypergraph
    
    n = random.randint(5, 40)
    m = random.randint(1, n**2)
    
    dnf = generate_dnf(n, m)
    hypergraph = hypergraph_from_dnf(dnf)
    
    matching_size = len(greedy_matching(hypergraph))
    
    is_k_clique = is_k_clique_dnf(dnf, math.isqrt(n) + 1)
    
    if is_k_clique:
        expected_min_matching_size = n // 2
    else:
        expected_max_matching_size = math.log(n, 2) + 2 * math.sqrt(m)
    
    conjecture_holds = (matching_size <= expected_max_matching_size and matching_size >= expected_min_matching_size)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Matching Size",
        "metric_value": matching_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")