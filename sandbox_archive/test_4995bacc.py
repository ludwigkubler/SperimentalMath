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
    
    def xor_and_tree(n):
        if n == 1:
            return [0, 1]
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return [left[i] ^ right[i] for i in range(len(left))]
    
    def hodge_decomposition(tree):
        if len(tree) == 1:
            return [1]
        else:
            left_hodge = hodge_decomposition(tree[:len(tree)//2])
            right_hodge = hodge_decomposition(tree[len(tree)//2:])
            return [left_hodge[i] + right_hodge[i] for i in range(len(left_hodge))]
    
    n = random.randint(5, 40)
    tree = xor_and_tree(n)
    hodge_order = len(hodge_decomposition(tree))
    
    metric_name = "hodge_order"
    metric_value = hodge_order
    instances_tested = 1
    conjecture_holds = (n**(1/3) <= hodge_order <= n**(4/5))
    counterexample = "" if conjecture_holds else f"hodge_order={hodge_order}, expected=[{int(n**(1/3))}, {int(n**(4/5))}]"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{r['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")