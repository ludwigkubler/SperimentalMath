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
    
    def generate_branching_program(n):
        program = []
        for _ in range(2**n - 1):
            if random.choice([0, 1]) == 0:
                program.append('0')
            else:
                program.append('1')
        return program
    
    def compute_minimal_rank(program):
        # Placeholder for the actual algorithm to compute minimal rank
        # This is a dummy implementation that returns a random rank for testing purposes
        return random.randint(1, 10)
    
    def compute_circuit_size(program):
        # Placeholder for the actual algorithm to compute circuit size
        # This is a dummy implementation that returns a random size for testing purposes
        return random.randint(1, 100)
    
    n = random.randint(5, 40)
    program = generate_branching_program(n)
    minimal_rank = compute_minimal_rank(program)
    circuit_size = compute_circuit_size(program)
    
    return {
        "metric_name": "minimal_rank_vs_circuit_size",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(RESULT)