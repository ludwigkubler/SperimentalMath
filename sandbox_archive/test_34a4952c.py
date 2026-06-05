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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['input']
        else:
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [f'AND({left[0]}, {right[0]})', f'OR({left[0]}, {right[0]})']
    
    def count_nodes(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            return 1 + sum(count_nodes(sub_circuit) for sub_circuit in circuit)
    
    depths = [5, 10]
    total_nodes = 0
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        for _ in range(3):
            circuit = generate_circuit(depth)
            nodes = count_nodes(circuit)
            if nodes > n_max:
                n_max = nodes
            total_nodes += nodes
            instances_tested += 1
    
    conjecture_holds = all(nodes <= 2 * depth**3 for depth in depths for _ in range(3))
    counterexample = "Depth {}, Nodes {}".format(depths[0], total_nodes) if not conjecture_holds else ""
    
    return {
        "metric_name": "Total Nodes",
        "metric_value": total_nodes,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")