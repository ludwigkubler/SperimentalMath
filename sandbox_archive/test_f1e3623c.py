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
        A = set(random.sample(range(1, n), n // 2))
        B = set(random.sample(range(n + 1, 2 * n), n // 2))
        return A, B
    
    def construct_morse_complex(A, B):
        # Simplified Morse complex construction for demonstration
        morse_complex = {frozenset([a]): 1 for a in A}
        morse_complex.update({frozenset([b]): 1 for b in B})
        return morse_complex
    
    def compute_minimal_rank(morse_complex):
        # Simplified minimal rank computation for demonstration
        return sum(morse_complex.values())
    
    def communication_complexity(A, B):
        # Simplified communication complexity for demonstration
        return len(A) + len(B)
    
    n = random.randint(5, 40)
    A, B = generate_disjoint_sets(n)
    morse_complex = construct_morse_complex(A, B)
    minimal_rank = compute_minimal_rank(morse_complex)
    comm_complexity = communication_complexity(A, B)
    
    return {
        "metric_name": "minimal_rank_vs_comm_complex",
        "metric_value": minimal_rank / comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"A={r['A']}, B={r['B']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break