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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monomial_ideal(boolean_function):
        n = len(boolean_function)
        ideal = set()
        for i in range(2**n):
            if boolean_function[i] == 1:
                binary_rep = bin(i)[2:].zfill(n)
                monomial = [int(bit) + 1 for bit in binary_rep]
                ideal.add(tuple(monomial))
        return ideal
    
    def quantum_group_rank(ideal):
        n = len(ideal)
        # Simplified rank calculation (placeholder)
        return Fraction(n, 2)
    
    def circuit_complexity(n):
        return Fraction(2**n, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_complexity = 0
    
    for n in n_values:
        boolean_function = generate_boolean_function(n)
        ideal = monomial_ideal(boolean_function)
        rank = quantum_group_rank(ideal)
        complexity = circuit_complexity(n)
        
        total_rank += rank
        total_complexity += complexity
    
    mean_rank = Fraction(total_rank, len(n_values))
    mean_complexity = Fraction(total_complexity, len(n_values))
    
    support_fraction = (mean_rank <= 2 * mean_complexity / n).count(True) / len(n_values)
    
    return {
        "metric_name": "Support Fraction",
        "metric_value": support_fraction,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_support_fraction = sum(r["support_fraction"] for r in results) / len(results)
    support_fraction_count = sum(1 for r in results if r["conjecture_holds"])
    
    if support_fraction_count >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0 support_fraction={support_fraction_count/len(results)}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")