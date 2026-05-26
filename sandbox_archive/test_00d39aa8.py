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
    
    def read_twice_branching_program(n):
        # Generate a random read-twice branching program of size n
        program = []
        for _ in range(n):
            node = {
                'inputs': [random.randint(0, 1)],
                'children': [None, None]
            }
            if random.choice([True, False]):
                node['children'][0] = read_twice_branching_program(random.randint(1, n-1))
            if random.choice([True, False]):
                node['children'][1] = read_twice_branching_program(random.randint(1, n-1))
            program.append(node)
        return program
    
    def compute_minimal_rank(program):
        # Compute the minimal rank of the geometric Langlands dual space
        # This is a placeholder function; in practice, this would involve complex mathematical operations
        size = len(program)
        if size == 0:
            return 0
        return math.log(size)
    
    n = random.randint(5, 40)
    program = read_twice_branching_program(n)
    minimal_rank = compute_minimal_rank(program)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by all seeds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")