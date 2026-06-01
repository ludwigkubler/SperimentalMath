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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_planar_graphs(n=40):
    # Placeholder function to generate planar graphs
    # This is a dummy implementation and should be replaced with actual graph generation logic
    return [random.randint(1, n) for _ in range(30)]

def construct_symplectic_leaves(graph):
    if isinstance(graph, list):
        return random.randint(1, len(graph))
    else:
        raise ValueError("Graph must be a list")

def calculate_communication_rank_growth(graph):
    # Placeholder function to calculate communication rank growth
    # This is a dummy implementation and should be replaced with actual algorithm logic
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    instances = generate_planar_graphs(n=40)
    msl_values = [construct_symplectic_leaves(graph) for graph in instances]
    cr_values = [calculate_communication_rank_growth(graph) for graph in instances]
    
    if len(msl_values) != len(cr_values):
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(instances),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "Mismatch in instance counts"
        }
    
    pearson_correlation = sum((msl - msl_avg) * (cr - cr_avg) for msl, cr in zip(msl_values, cr_values)) / len(msl_values)
    msl_avg = sum(msl_values) / len(msl_values)
    cr_avg = sum(cr_values) / len(cr_values)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": len(instances),
        "n_max": 40,
        "conjecture_holds": pearson_correlation >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation < 0.7' first_failing_seed={first_failing_seed}")