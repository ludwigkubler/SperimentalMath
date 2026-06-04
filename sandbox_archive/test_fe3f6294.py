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
    
    def generate_symmetric_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[2**i] != f[2**j]:
                    rank += 1
        return rank
    
    def symplectic_grassmannian_order(f):
        # Placeholder function for computing the minimal order of leaves
        # This is a dummy implementation and should be replaced with actual computation
        n = int(math.log2(len(f)))
        return n // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_symmetric_boolean_function(n)
        mol = symplectic_grassmannian_order(f)
        rank = communication_complexity_rank(f)
        results.append((mol, rank))
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "communication_complexity_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mol_values = [mol for mol, _ in results]
    rank_values = [rank for _, rank in results]
    
    n_max = max([len(mol_values), len(rank_values)])
    instances_tested = len(results)
    
    if instances_tested < 30:
        return {
            "seed": seed,
            "metric_name": "communication_complexity_rank",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_mol = sum(mol_values) / instances_tested
    mean_rank = sum(rank_values) / instances_tested
    
    correlation_coefficient = 0.0
    if len(mol_values) > 1 and len(rank_values) > 1:
        numerator = sum((mol - mean_mol) * (rank - mean_rank) for mol, rank in results)
        denominator = math.sqrt(sum((mol - mean_mol) ** 2 for mol in mol_values)) * math.sqrt(sum((rank - mean_rank) ** 2 for rank in rank_values))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "seed": seed,
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")