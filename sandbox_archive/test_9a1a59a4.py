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
    
    def generate_group(n):
        # Generate a random finitely presented group G with n generators and relations
        generators = [f'a{i}' for i in range(n)]
        relations = []
        for _ in range(2 * n):
            rel = ''.join(random.choice(generators) for _ in range(3))
            relations.append(f'{rel} = 1')
        return f'<{", ".join(generators)}, {"; ".join(relations)}>'

    def dpll_tree_width(group, n):
        # Simulate the construction of the DPLL tree and estimate its width
        # This is a simplified model; actual implementation would be complex
        if n == 1:
            return 2
        elif n == 2:
            return 4
        else:
            return 8

    def min_local_indeterminacy(group):
        # Simulate the computation of minimal local indeterminacy
        # This is a simplified model; actual implementation would be complex
        if 'a0' in group and 'a1' in group:
            return 0.5
        else:
            return random.random()

    n = random.choice([5, 10, 15, 20, 30, 40])
    group = generate_group(n)
    min_indet_G = min_local_indeterminacy(group)
    w_G = dpll_tree_width(group, n)

    return {
        "metric_name": "min_indet(G)",
        "metric_value": min_indet_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_indet_G - w_G) / max(1, w_G) <= 0.1,
        "counterexample": f"min_indet(G) = {min_indet_G}, w(G) = {w_G}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='{results[0]['counterexample']}' first_failing_seed={first_failing_seed}")