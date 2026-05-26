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
    instances_tested = 30
    total_order = 0
    
    for _ in range(instances_tested):
        # Generate a random n-bit input
        input_bits = [random.choice([0, 1]) for _ in range(n)]
        
        # Construct the corresponding XOR-AND tree
        def xor_and_tree(bits):
            if len(bits) == 1:
                return bits[0]
            mid = len(bits) // 2
            left = xor_and_tree(bits[:mid])
            right = xor_and_tree(bits[mid:])
            return left ^ right
        
        tree = xor_and_tree(input_bits)
        
        # Compute the Hodge decomposition (simplified for demonstration)
        def hodge_decomposition(tree):
            if isinstance(tree, int):
                return 1
            else:
                return hodge_decomposition(tree[0]) + hodge_decomposition(tree[1])
        
        order = hodge_decomposition(tree)
        total_order += order
    
    mean_order = total_order / instances_tested
    conjecture_holds = Ω_n_1_3 <= mean_order <= O_n_4_5
    counterexample = "" if conjecture_holds else f"mean_order={mean_order}, expected=[Ω(n^{1/3}), O(n^{4/5})]"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def main():
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")

if __name__ == "__main__":
    import sys
    main()