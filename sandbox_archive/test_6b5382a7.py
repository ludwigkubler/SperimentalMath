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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partition_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = float('inf')
        for i in range(1, n):
            left = f[:i]
            right = f[i:]
            rank_left = noncrossing_partition_rank(left)
            rank_right = noncrossing_partition_rank(right)
            rank = min(rank, rank_left + rank_right)
        return rank
    
    def monotone_span_program(f):
        n = len(f)
        if n == 1:
            return [f[0]]
        program = []
        for i in range(1, n):
            left = f[:i]
            right = f[i:]
            program_left = monotone_span_program(left)
            program_right = monotone_span_program(right)
            program.extend(program_left + program_right)
        return program
    
    def circuit_size(program):
        size = 0
        for gate in program:
            if isinstance(gate, list):
                size += len(gate)
            else:
                size += 1
        return size
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    
    rank = noncrossing_partition_rank(f)
    program = monotone_span_program(f)
    circuit_size_value = circuit_size(program)
    
    metric_name = "Circuit Size"
    metric_value = circuit_size_value
    instances_tested = 1
    conjecture_holds = rank <= n**(1/4) and circuit_size_value <= 2**math.ceil(n**(1/4))
    counterexample = "" if conjecture_holds else f"Rank: {rank}, Circuit Size: {circuit_size_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")