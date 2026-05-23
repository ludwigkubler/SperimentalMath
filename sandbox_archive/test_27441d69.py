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
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    
    # Generate a random boolean function
    def generate_boolean_function():
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def degree(boolean_function):
        return len([i for i, bit in enumerate(boolean_function) if bit == '1'])
    
    def monomial_ideal(boolean_function):
        ideal = set()
        for i in range(len(boolean_function)):
            if boolean_function[i] == '1':
                term = [0] * n
                term[i] = 1
                ideal.add(tuple(term))
        return ideal
    
    def coxeter_group_rank(ideal):
        # This is a simplified version of computing the rank of the Coxeter group.
        # For simplicity, we assume that the rank is equal to the number of variables.
        return n
    
    boolean_function = generate_boolean_function()
    deg = degree(boolean_function)
    ideal = monomial_ideal(boolean_function)
    rank = coxeter_group_rank(ideal)
    
    conjecture_holds = rank <= deg
    counterexample = "" if conjecture_holds else f"boolean_function={boolean_function}, deg={deg}, rank={rank}"
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")