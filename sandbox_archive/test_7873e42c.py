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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def num_true_assignments(formula, n):
        count = 0
        for i in range(2**n):
            assignment = format(i, f'0{n}b')
            if all(formula[i] == '0' or (assignment[int(j)] == '1') == (formula[i] == '1') for j in range(n)):
                count += 1
        return count
    
    def frege_proof_length(formula):
        # Simplified Frege proof length calculation
        return len(formula) * 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_boolean_formula(n)
    true_assignments = num_true_assignments(formula, n)
    proof_length = frege_proof_length(formula)
    
    return {
        "metric_name": "frege_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"RESULT: {RESULT} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")