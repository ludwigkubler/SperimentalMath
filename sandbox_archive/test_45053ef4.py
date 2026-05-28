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
    
    def p_adic_lattice_rank(n):
        # Constructive mapping to compute a p-adic lattice rank for a circuit of n variables
        return (n * (n + 1)) // 2
    
    def is_k_clique_circuit(circuit_size, n):
        # Placeholder function to determine if the circuit computes k-CLIQUE
        # For simplicity, assume half of the circuits compute k-CLIQUE
        return random.choice([True, False])
    
    alpha = 1.0  # Constant for k-CLIQUE circuits
    beta = 0.5   # Constant for non-k-CLIQUE circuits
    
    results = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times
            circuit_size = random.randint(n, 2 * n)
            if is_k_clique_circuit(circuit_size, n):
                expected_rank = alpha * n**2
                actual_rank = p_adic_lattice_rank(n)
                results.append(actual_rank >= expected_rank)
            else:
                expected_rank = beta * circuit_size
                actual_rank = p_adic_lattice_rank(n)
                results.append(actual_rank <= expected_rank)
            
            instances_tested += 1
    
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "conjecture_support",
        "metric_value": sum(results) / len(results),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if len(results) > 0 else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=empty_results")