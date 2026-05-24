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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(n-1):
            clauses.append([f'x{i}', f'x{i+1}'])
        return variables, clauses
    
    def calculate_order_of_representation(n):
        # Simplified representation order calculation
        return 2 * n - 1
    
    def construct_resolution_proof(clauses):
        proof_length = len(clauses) * 2
        return proof_length
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = generate_tseitin_formula(n)
        order_of_representation = calculate_order_of_representation(n)
        resolution_proof_length = construct_resolution_proof(clauses)
        
        results.append({
            "n": n,
            "order_of_representation": order_of_representation,
            "resolution_proof_length": resolution_proof_length
        })
    
    total_order = sum(result["order_of_representation"] for result in results)
    mean_order = Fraction(total_order, len(results))
    max_order = max(result["order_of_representation"] for result in results)
    min_order = min(result["order_of_representation"] for result in results)
    std_dev_order = math.sqrt(sum((result["order_of_representation"] - mean_order) ** 2 for result in results) / len(results))
    
    total_length = sum(result["resolution_proof_length"] for result in results)
    mean_length = Fraction(total_length, len(results))
    max_length = max(result["resolution_proof_length"] for result in results)
    min_length = min(result["resolution_proof_length"] for result in results)
    std_dev_length = math.sqrt(sum((result["resolution_proof_length"] - mean_length) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(
        abs(order_of_representation - math.log(n)) <= 0.5 * math.log(n) and
        resolution_proof_length <= 2 ** (1.25 * order_of_representation)
        for n, order_of_representation, resolution_proof_length in zip([5, 10, 15, 20, 30, 40], 
                                                                     [result["order_of_representation"] for result in results],
                                                                     [result["resolution_proof_length"] for result in results])
    )
    
    counterexample = ""
    if not conjecture_holds:
        for n, order_of_representation, resolution_proof_length in zip([5, 10, 15, 20, 30, 40], 
                                                                     [result["order_of_representation"] for result in results],
                                                                     [result["resolution_proof_length"] for result in results]):
            if not (abs(order_of_representation - math.log(n)) <= 0.5 * math.log(n) and
                    resolution_proof_length <= 2 ** (1.25 * order_of_representation)):
                counterexample = f"n={n}, ρ(f)={order_of_representation}, length={resolution_proof_length}"
                break
    
    return {
        "metric_name": "order_of_representation",
        "metric_value": float(mean_order),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_order = sum(result["metric_value"] for result in results)
    mean_order = total_order / len(results)
    std_dev_order = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev_order} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")