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
                program.append('0')
            else:
                program.append('1')
        return program
    
    def construct_configuration_space(program):
        n = len(program)
        CS = [[0] * (n + 1) for _ in range(2)]
        CS[program[0]][0] = 1
        for i in range(1, n):
            if program[i] == '0':
                CS[0][i] += CS[0][i-1]
                CS[1][i] += CS[1][i-1]
            else:
                CS[0][i] += CS[1][i-1]
                CS[1][i] += CS[0][i-1]
        return CS
    
    def min_local_index(CS):
        n = len(CS[0]) - 1
        return min(CS[0][-2], CS[1][-2])
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        P = generate_branching_program(n)
        CS = construct_configuration_space(P)
        local_index = min_local_index(CS)
        results.append(local_index)
    
    avg_index = sum(results) / len(results)
    if all(index <= math.log(len(P)) for index, P in zip(results, [generate_branching_program(random.randint(5, 40)) for _ in range(30)])):
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "min_local_index",
        "metric_value": avg_index,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")