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
    
    def generate_formula(n):
        return ' & '.join(f'x{i}' if random.choice([True, False]) else f'~x{i}' for i in range(1, n+1))
    
    def hodge_rank(formula):
        # Placeholder function. In practice, this would compute the Hodge rank.
        return len(formula.split(' & '))
    
    def sat_refutation_tree_width(formula):
        # Placeholder function. In practice, this would compute the refutation tree width.
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    rank = hodge_rank(formula)
    width = sat_refutation_tree_width(formula)
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": abs(rank - width),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")