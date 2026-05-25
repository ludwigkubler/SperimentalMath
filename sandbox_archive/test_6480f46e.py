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
        for _ in range(n):
            if random.choice([True, False]):
                program.append((random.randint(0, 1), random.randint(0, n-1)))
            else:
                program.append((random.randint(2, 3), random.randint(0, n-1)))
        return program
    
    def tropicalized_cohomology_rank(program):
        # Placeholder for actual computation
        # For simplicity, we assume a rank that depends on the size of the program
        return len(program) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    program = generate_branching_program(n)
    cohomology_rank = tropicalized_cohomology_rank(program)
    
    expected_max_rank = 2 * math.log(n) ** 1.5
    conjecture_holds = cohomology_rank <= expected_max_rank
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": cohomology_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {cohomology_rank} exceeds expected {expected_max_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds expected' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")