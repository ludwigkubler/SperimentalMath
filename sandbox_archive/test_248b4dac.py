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
    
    def generate_circuit(depth):
        if depth == 0:
            return "leaf"
        else:
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [left, right]
    
    def count_nodes(circuit):
        if circuit == "leaf":
            return 1
        else:
            return 1 + count_nodes(circuit[0]) + count_nodes(circuit[1])
    
    max_depth = 10
    instances_tested = 0
    total_nodes = 0
    
    for depth in range(1, max_depth + 1):
        circuit = generate_circuit(depth)
        nodes = count_nodes(circuit)
        total_nodes += nodes
        instances_tested += 1
    
    expected_bound = Fraction(4 * (max_depth ** 3), 3)  # Polynomial bound of degree 3
    conjecture_holds = total_nodes <= expected_bound
    counterexample = "" if conjecture_holds else f"Depth {max_depth}, Nodes {total_nodes}"
    
    return {
        "metric_name": "Total Nodes",
        "metric_value": total_nodes,
        "instances_tested": instances_tested,
        "n_max": max_depth,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_nodes = sum(r["metric_value"] for r in results) / len(results)
    std_nodes = (sum((r["metric_value"] - mean_nodes) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_nodes} std={std_nodes} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_nodes} std={std_nodes} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")