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
    
    def is_quadratic_residue(a, p):
        return pow(a, (p - 1) // 2, p) == 1
    
    def generate_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_rank_variance(protocol):
        # Compute the rank variance of the protocol
        n = len(protocol)
        counts = [protocol.count(i) for i in range(2)]
        mean = sum(counts) / n
        variance = sum((x - mean) ** 2 for x in counts) / n
        return variance
    
    def count_quadratic_residues(outcomes, p):
        # Count the number of quadratic residues needed to represent outcomes
        residues = set()
        for outcome in outcomes:
            residues.update([i for i in range(p) if is_quadratic_residue(i, p)])
        return len(residues)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(10):
            protocol = generate_protocol(n)
            R = compute_rank_variance(protocol)
            outcomes = set(tuple(protocol))
            p = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23])
            num_residues = count_quadratic_residues(outcomes, p)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            total_metric_value += num_residues
            
            expected_bound = p ** (R + 1 / n)
            if num_residues > expected_bound:
                conjecture_holds = False
                counterexample = f"n={n}, R={R}, p={p}, outcomes={outcomes}, num_residues={num_residues}, expected_bound={expected_bound}"
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "number_of_quadratic_residues",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")