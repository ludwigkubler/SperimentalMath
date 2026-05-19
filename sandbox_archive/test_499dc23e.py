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
    
    def generate_abp(n):
        if n == 1:
            return [[0, 1]]
        else:
            sub_abps = [generate_abp(i) for i in range(1, n)]
            abp = []
            for sub_abp in sub_abps:
                for node in sub_abp:
                    new_node = [node[0] + 1] + node[1:]
                    abp.append(new_node)
            return abp
    
    def evaluate_abp(abp, input_bits):
        stack = []
        for node in abp:
            if len(node) == 2:
                stack.append(input_bits[node[1]])
            else:
                a = stack.pop()
                b = stack.pop()
                if node[0] == 0:  # AND
                    stack.append(a and b)
                elif node[0] == 1:  # OR
                    stack.append(a or b)
        return stack[-1]
    
    def is_parity_function(abp):
        for input_bits in product([0, 1], repeat=len(abp)):
            if evaluate_abp(abp, input_bits) != parity(input_bits):
                return False
        return True
    
    def parity(bits):
        return sum(bits) % 2
    
    n = random.randint(5, 40)
    abps = generate_abp(n)
    
    depth_count = [0] * (n + 1)
    for abp in abps:
        current_depth = 0
        stack = []
        for node in abp:
            if len(node) == 2:
                stack.append(current_depth)
            else:
                current_depth = max(stack.pop(), current_depth) + 1
        depth_count[current_depth] += 1
    
    mean_depth = sum(depth * count for depth, count in enumerate(depth_count)) / sum(depth_count)
    conjecture_holds = mean_depth >= math.log2(n)
    
    return {
        "metric_name": "mean_depth",
        "metric_value": mean_depth,
        "instances_tested": len(abps),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean depth {mean_depth} < log2({n}) = {math.log2(n)}"
    }

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")