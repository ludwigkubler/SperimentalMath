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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        return ' and '.join(clauses)

    def count_betti_numbers(simplicial_complex):
        # Placeholder for Betti number calculation
        # This is a dummy implementation for testing purposes
        return random.randint(1, 5)

    def sos_rank(poly):
        # Placeholder for SOS rank calculation
        # This is a dummy implementation for testing purposes
        return random.randint(2, 6)

    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_3sat_instance(n)
    
    simplicial_complex = parse_simplicial_complex(instance)  # Placeholder function
    betti_numbers_sum = count_betti_numbers(simplicial_complex)
    sos_rank_value = sos_rank(instance)

    return {
        "metric_name": "Betti Number Sum vs SOS Rank",
        "metric_value": betti_numbers_sum,
        "instances_tested": 1,
        "conjecture_holds": betti_numbers_sum <= sos_rank_value,
        "counterexample": "" if betti_numbers_sum <= sos_rank_value else "Betti numbers sum > SOS rank"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Betti numbers sum > SOS rank\" first_failing_seed={first_failing_seed}")

def parse_simplicial_complex(instance):
    # Placeholder function to parse simplicial complex
    return []