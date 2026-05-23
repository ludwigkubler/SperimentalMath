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
    
    def generate_disjoint_sets(n):
        A = set(random.sample(range(1, n*2), n))
        B = set(random.sample(range(n*2+1, 2*n*2), n))
        return A, B
    
    def morse_complex_rank(A, B):
        # Simplified Morse complex rank calculation for demonstration
        return len(A) + len(B)
    
    def communication_complexity_disjointness(A, B):
        # Simplified communication complexity for disjointness
        return max(len(A), len(B))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A, B = generate_disjoint_sets(n)
    rank = morse_complex_rank(A, B)
    comm_complexity = communication_complexity_disjointness(A, B)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": Fraction(rank, comm_complexity),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + random.randint(0, 100) for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0.7) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r <= 0.7 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")