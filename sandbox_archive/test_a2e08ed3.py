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

def generate_planar_graphs(n):
    if n == 1:
        return [([(0, 0)], [])]
    elif n == 2:
        return [([(0, 0), (1, 0)], [(0, 1)]),
                ([(0, 0), (0, 1)], [(1, 0)])]
    else:
        graphs = []
        for i in range(n):
            for j in range(i + 1, n):
                new_nodes = [(i, 0), (j, 0)]
                new_edges = [(0, 1)]
                if i != 0 and j != n - 1:
                    new_edges.append((1, 0))
                graphs.append((new_nodes, new_edges))
        return graphs

def construct_symplectic_leaves(graph):
    nodes, edges = graph
    msl = len(nodes)
    return msl

def calculate_communication_rank_growth(graph):
    nodes, edges = graph
    cr = len(edges) + 1
    return cr

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    instances = generate_planar_graphs(40)
    msl_values = [construct_symplectic_leaves(graph) for graph in instances]
    cr_values = [calculate_communication_rank_growth(graph) for graph in instances]
    
    if not msl_values or not cr_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(instances),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "empty_input"
        }
    
    pearson_correlation = sum((x - msl_avg) * (y - cr_avg) for x, y in zip(msl_values, cr_values)) / len(instances)
    msl_avg = sum(msl_values) / len(instances)
    cr_avg = sum(cr_values) / len(instances)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": len(instances),
        "n_max": 40,
        "conjecture_holds": abs(pearson_correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")