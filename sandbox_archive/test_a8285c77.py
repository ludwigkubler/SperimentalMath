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

def generate_random_program(n):
    program = []
    for _ in range(n):
        if random.choice([True, False]):
            program.append((random.randint(0, n-1), None))
        else:
            program.append((None, random.randint(0, n-1)))
    return program

def compute_minimal_rank(program):
    if not any(j == i for j, _ in program if j is not None and _ is not None):
        return 0
    rank = 0
    visited = set()
    stack = []
    for node, edge in program:
        if node is not None and node not in visited:
            rank += 1
            stack.append(node)
            while stack:
                current = stack.pop()
                visited.add(current)
                for next_node, _ in program:
                    if next_node == current:
                        stack.append(next_node)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    program = generate_random_program(n)
    rank = compute_minimal_rank(program)
    g_n = math.log2(2**n + n)
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= g_n,
        "counterexample": "" if rank <= g_n else f"Rank {rank} exceeds bound {g_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")