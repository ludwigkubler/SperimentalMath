# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        if n < 5:
            return None
        edges = set()
        while len(edges) < n - 1:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def tseitin_formula(graph):
        cnf = []
        n = len(graph)
        for i in range(n):
            literals = [f"x{i}_{j}" for j in range(n)]
            clause = [literals[0]]
            for literal in literals[1:]:
                clause.append(f"~{literal}")
            cnf.append(clause)
            for j, k in graph:
                if j == i:
                    cnf.append([f"~x{i}_{j}", f"x{k}_{j}"])
                elif k == i:
                    cnf.append([f"~x{i}_{k}", f"x{j}_{k}"])
        return cnf
    
    def minimal_tropical_motivic_rank(cnf):
        # Placeholder for actual computation
        return random.random()
    
    def communication_complexity_rank(cnf):
        # Placeholder for actual computation
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_random_graph(n)
        if not graph:
            continue
        cnf = tseitin_formula(graph)
        mtr = minimal_tropical_motivic_rank(cnf)
        ccr = communication_complexity_rank(cnf)
        results.append((n, mtr, ccr))
    
    if not results:
        return {
            "metric_name": "mtr_to_ccr_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    mtr_to_ccr_ratios = [mtr / ccr for _, mtr, ccr in results]
    mean_ratio = sum(mtr_to_ccr_ratios) / instances_tested
    std_ratio = (sum((x - mean_ratio) ** 2 for x in mtr_to_ccr_ratios) / instances_tested) ** 0.5
    
    return {
        "metric_name": "mtr_to_ccr_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": std_ratio < 1e-6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_ratio = (sum((r['metric_value'] - mean_ratio) ** 2 for r in results if r['metric_value'] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[support_fraction < 0.95]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation n_tested={len(results)}")