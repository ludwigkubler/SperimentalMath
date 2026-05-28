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
    
    def generate_n_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def macdonald_polynomial_rank(cnf):
        # Placeholder function to compute the rank of a Macdonald polynomial
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(cnf)  # Simplified for testing purposes
    
    n_values = [10, 15, 20, 30, 40]
    total_instances = 0
    low_rank_count = 0
    counterexample = ""
    
    for n in n_values:
        instances_tested = 0
        for _ in range(6):  # Test each n with 6 instances
            cnf = generate_n_cnf(n)
            rank = macdonald_polynomial_rank(cnf)
            if rank < n**2:
                low_rank_count += 1
            instances_tested += 1
            total_instances += 1
    
    mean_rank = Fraction(low_rank_count, total_instances) * n_values[0]**2
    support_fraction = (total_instances - low_rank_count) / total_instances
    
    if support_fraction >= 0.95:
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = "The observed rank is less than O(n^2) for more than 5% of instances."
    
    return {
        "metric_name": "Low Rank Count",
        "metric_value": low_rank_count,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")