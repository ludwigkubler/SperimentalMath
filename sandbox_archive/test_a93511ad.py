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
    
    def quantum_entropy(n):
        return n * math.log2(n)
    
    def xor_and_tree_width(n):
        if n == 1:
            return 1
        return 2 * xor_and_tree_width(n // 2) + 1
    
    def generate_branching_program(n):
        program = []
        for _ in range(n):
            program.append(random.choice(['0', '1']))
        return program
    
    def compute_quantum_entropy(program):
        n = len(program)
        entropy = quantum_entropy(n)
        return entropy
    
    def construct_xor_and_tree(program):
        n = len(program)
        if n == 1:
            return [program[0]]
        left_tree = construct_xor_and_tree(program[:n//2])
        right_tree = construct_xor_and_tree(program[n//2:])
        return ['XOR'] + left_tree + right_tree
    
    def tree_width(tree):
        if isinstance(tree, str):
            return 1
        return max(tree_width(child) for child in tree[1:]) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            program = generate_branching_program(n)
            entropy = compute_quantum_entropy(program)
            tree = construct_xor_and_tree(program)
            width = tree_width(tree)
            
            total_entropy += entropy
            total_width += width
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    mean_width = total_width / instances_tested
    
    if mean_entropy <= math.log2(instances_tested) and mean_width >= instances_tested:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Counterexample found: Mean entropy <= log(n) and mean width >= n"
    
    return {
        "metric_name": "Quantum Entropy vs XOR-AND Tree Width",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")