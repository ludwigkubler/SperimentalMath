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
    
    def generate_branching_program(n):
        program = []
        for _ in range(2**n - 1):
            if random.randint(0, 1):
                program.append(random.choice([0, 1]))
            else:
                program.extend(random.sample(range(n), 2))
        return program
    
    def compute_minimal_rank(program):
        n = len(program) // (2**(len(program) + 1))
        rank = sum(1 for bit in program if bit == 1)
        return rank
    
    def compute_circuit_size(program):
        n = len(program) // (2**(len(program) + 1))
        size = 0
        stack = []
        for bit in program:
            if bit == 0:
                stack.append(bit)
            else:
                a, b = random.sample(range(n), 2)
                stack.append((a, b))
                size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    sizes = []
    
    for n in n_values:
        program = generate_branching_program(n)
        rank = compute_minimal_rank(program)
        size = compute_circuit_size(program)
        ranks.append(rank)
        sizes.append(size)
    
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (sizes[i] - mean(sizes)) for i in range(len(ranks))) / math.sqrt(sum((ranks[i] - mean(ranks))**2 for i in range(len(ranks)))) / math.sqrt(sum((sizes[i] - mean(sizes))**2 for i in range(len(sizes))))
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")