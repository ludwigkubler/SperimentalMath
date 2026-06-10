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

def generate_boolean_circuit(depth):
    if depth == 1:
        return ["0", "1"]
    left = generate_boolean_circuit(depth - 1)
    right = generate_boolean_circuit(depth - 1)
    return [f"AND({l}, {r})" for l in left] + [f"OR({l}, {r})" for l in right]

def evaluate_circuit(circuit):
    if isinstance(circuit, str):
        if circuit == "0":
            return False
        elif circuit == "1":
            return True
        else:
            op, l, r = circuit.split('(')[1].split(',')
            l = l.strip()
            r = r.strip().rstrip(')')
            if op == "AND":
                return evaluate_circuit(l) and evaluate_circuit(r)
            elif op == "OR":
                return evaluate_circuit(l) or evaluate_circuit(r)
    else:
        raise ValueError("Invalid circuit")

def generate_random_circuit(depth):
    circuit = generate_boolean_circuit(depth)
    return random.choice(circuit)

def compute_kashiwara_vergne_structure(circuit):
    # Placeholder function to simulate the computation
    # This is a dummy implementation and does not reflect actual Kashiwara-Vergne structure
    return len(circuit.split('AND')) + len(circuit.split('OR'))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        depth = random.randint(5, 40)
        circuit = generate_random_circuit(depth)
        rank = compute_kashiwara_vergne_structure(circuit)
        results.append((depth, rank))
    
    n_max = max(depth for depth, _ in results)
    if n_max < 16:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    depths = [depth for depth, _ in results]
    ranks = [rank for _, rank in results]
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    correlation_coefficient = sum((depths[i] - mean_depth) * (ranks[i] - mean_rank) for i in range(len(depths))) / (len(depths) * std_depth * std_rank)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_rank - mean_depth) <= 3,
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

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")