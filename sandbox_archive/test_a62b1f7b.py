# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_branching_program(n):
        width = random.randint(2, n)
        depth = random.randint(1, 5)
        program = []
        for _ in range(depth):
            level = [random.choice([0, 1]) for _ in range(width)]
            program.append(level)
        return program
    
    def compute_hodge_structure(program):
        width = len(program[0])
        height = len(program)
        hodge_matrix = [[0] * (width + 1) for _ in range(height + 1)]
        
        for i in range(1, height + 1):
            for j in range(1, width + 1):
                if program[i-1][j-1] == 0:
                    hodge_matrix[i][j] = hodge_matrix[i-1][j-1]
                else:
                    hodge_matrix[i][j] = hodge_matrix[i-1][j-1] + 1
        
        return hodge_matrix
    
    def minimal_rank(hodge_matrix):
        rank = 0
        for row in hodge_matrix:
            if any(row[j] > 0 for j in range(len(row))):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    program = generate_branching_program(n)
    width_value = len(program[0])
    
    hodge_structure = compute_hodge_structure(program)
    minimal_rank_value = minimal_rank(hodge_structure)
    
    conjecture_holds = abs(minimal_rank_value - width_value) <= 3 and minimal_rank_value <= 10
    counterexample = "" if conjecture_holds else f"rank={minimal_rank_value}, expected={width_value}"
    
    return {
        "metric_name": "MinimalRank",
        "metric_value": minimal_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_count = sum(1 for r in results if r["conjecture_holds"])
    
    if support_count >= 24:
        result_status = "SUPPORTED"
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result_status = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    else:
        result_status = "INCONCLUSIVE"
    
    print(f"RESULT: {result_status} mean={mean_value:.2f} std={std_value:.2f} support_fraction={(support_count / len(results)):.2f}")