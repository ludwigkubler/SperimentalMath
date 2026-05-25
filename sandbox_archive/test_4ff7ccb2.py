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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_once_branching_program(n):
        program = []
        for _ in range(n):
            if random.choice([True, False]):
                program.append('0')
            else:
                program.append('1')
        return program
    
    def construct_configuration_space(program):
        n = len(program)
        CS = [[[] for _ in range(2)] for _ in range(n)]
        CS[program[0]][0] = 1
        CS[program[0]][1] = 1
        
        for i in range(1, n):
            if program[i] == '0':
                CS[program[i]][0].extend(CS[program[i-1]][0])
                CS[program[i]][1].extend(CS[program[i-1]][1])
            else:
                CS[program[i]][0].extend(CS[program[i-1]][1])
                CS[program[i]][1].extend(CS[program[i-1]][0])
        
        return CS
    
    def min_local_index(CS):
        n = len(CS)
        indices = [len(CS[i][0]) + len(CS[i][1]) for i in range(n)]
        return min(indices)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        P = generate_read_once_branching_program(n)
        CS = construct_configuration_space(P)
        index = min_local_index(CS)
        results.append(index)
    
    avg_index = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - avg_index) ** 2 for x in results) / len(results))
    
    if all(5 <= n <= 40 for n in [len(P) for P in results]):
        support_fraction = Fraction(sum(1 for index in results if 0.9 * math.log(len(P)) <= index <= 1.1 * math.log(len(P))) + sum(1 for index in results if 0.95 * len(P) <= index <= 1.05 * len(P)), len(results))
    else:
        support_fraction = Fraction(sum(1 for index in results if 0.9 * math.log(len(P)) <= index <= 1.1 * math.log(len(P))), len(results))
    
    conjecture_holds = support_fraction >= Fraction(8, 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_local_index",
        "metric_value": avg_index,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_index = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_index) ** 2 for result in results) / len(results))
    support_fraction = Fraction(sum(1 for result in results if result["conjecture_holds"]), len(results))
    
    if support_fraction >= Fraction(8, 10):
        print(f"RESULT: SUPPORTED mean={avg_index} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")