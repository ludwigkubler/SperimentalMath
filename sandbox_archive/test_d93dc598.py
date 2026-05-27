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
    
    def negation_width(circuit):
        if isinstance(circuit, str):
            return 1
        elif circuit[0] == 'AND':
            return max(negation_width(circuit[1]), negation_width(circuit[2]))
        elif circuit[0] == 'OR':
            return max(negation_width(circuit[1]), negation_width(circuit[2]))
        elif circuit[0] == 'NOT':
            return 1 + negation_width(circuit[1])
    
    def resolution_refutation_tree(circuit):
        if isinstance(circuit, str):
            return [circuit]
        elif circuit[0] == 'AND':
            left = resolution_refutation_tree(circuit[1])
            right = resolution_refutation_tree(circuit[2])
            return [f"NOT {x}" for x in left] + [f"NOT {y}" for y in right] + [f"{x} OR {y}" for x in left for y in right]
        elif circuit[0] == 'OR':
            left = resolution_refutation_tree(circuit[1])
            right = resolution_refutation_tree(circuit[2])
            return [f"NOT {x}" for x in left] + [f"NOT {y}" for y in right] + [f"{x} AND {y}" for x in left for y in right]
        elif circuit[0] == 'NOT':
            return resolution_refutation_tree(circuit[1])
    
    def tropicalized_hodge_structure(tree):
        if not tree:
            return 0
        if isinstance(tree, str):
            return 1
        else:
            return max(tropicalized_hodge_structure(x) for x in tree)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    width = negation_width(circuit)
    tree = resolution_refutation_tree(circuit)
    rank = tropicalized_hodge_structure(tree)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": width > 0 and rank >= width * math.log(width, 2),
        "counterexample": "" if width > 0 and rank >= width * math.log(width, 2) else f"width={width}, rank={rank}"
    }

def generate_random_circuit(n):
    if n == 1:
        return random.choice(['x', 'NOT x'])
    elif n == 2:
        op = random.choice(['AND', 'OR'])
        left = generate_random_circuit(1)
        right = generate_random_circuit(1)
        return (op, left, right)
    else:
        op = random.choice(['AND', 'OR'])
        left = generate_random_circuit(n // 2)
        right = generate_random_circuit(n - n // 2)
        return (op, left, right)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2**31, 2**64-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")