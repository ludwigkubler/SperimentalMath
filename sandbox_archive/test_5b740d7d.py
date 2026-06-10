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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ["0", "1"]
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return [f"AND({l}, {r})" for l in left] + [f"OR({l}, {r})" for l in left]
    
    def count_nodes(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            return sum(count_nodes(sub) for sub in circuit)
    
    def compute_rank(circuit):
        # Simplified rank computation based on the number of nodes
        return count_nodes(circuit)
    
    depth = random.randint(5, 40)
    circuit = generate_boolean_circuit(depth)
    rank = compute_rank(circuit)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": depth,
        "conjecture_holds": True if rank >= depth else False,
        "counterexample": "" if rank >= depth else f"Circuit with depth {depth} has rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["instances_tested"] > 0:
            results.append(result)
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8 and abs(mean_rank - sum(result["n_max"] for result in results) / len(results)) <= 3:
            print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='rank_too_low' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")