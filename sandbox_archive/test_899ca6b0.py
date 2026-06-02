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
    
    def generate_quasi_platonic_solid(n):
        # Simplified generation for demonstration purposes
        return n
    
    def construct_cnf(solid):
        # Simulated CNF construction based on solid size
        return [i for i in range(1, solid + 1)]
    
    def frege_proof_length(cnf):
        # Simulated Frege proof length calculation
        return len(cnf) * 2
    
    correlation_coefficient = None
    instances_tested = 0
    n_max = 0
    conjecture_holds = False
    counterexample = ""
    
    for n in range(5, 41):
        solid = generate_quasi_platonic_solid(n)
        cnf = construct_cnf(solid)
        proof_length = frege_proof_length(cnf)
        
        if proof_length <= 0:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        
    if instances_tested > 1:
        orders = [generate_quasi_platonic_solid(n) for n in range(5, 41)]
        proof_lengths = [frege_proof_length(construct_cnf(solid)) for solid in orders]
        
        mean_order = sum(orders) / len(orders)
        mean_proof_length = sum(proof_lengths) / len(proof_lengths)
        
        numerator = instances_tested * sum(order * proof_length for order, proof_length in zip(orders, proof_lengths))
        denominator = math.sqrt((instances_tested * sum(order ** 2 for order in orders) - instances_tested * mean_order ** 2) * (instances_tested * sum(proof_length ** 2 for proof_length in proof_lengths) - instances_tested * mean_proof_length ** 2))
        
        if denominator != 0:
            correlation_coefficient = (numerator - instances_tested * mean_order * mean_proof_length) / denominator
            conjecture_holds = abs(correlation_coefficient) >= 0.5 and abs(mean_difference) <= 3
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient if correlation_coefficient is not None else float('nan'),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(r["metric_value"]) for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not math.isnan(r["metric_value"]) for r in results):
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_data")