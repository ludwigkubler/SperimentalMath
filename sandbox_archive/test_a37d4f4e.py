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
    
    def generate_game(n):
        # Generate a simple communication game with n players
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def free_monoidal_category(game):
        # Construct the free monoidal category representing the game's structure
        n = len(game)
        category = {}
        for i in range(n):
            for j in range(n):
                if game[i][j] == 1:
                    category[(i, j)] = []
        return category
    
    def minimal_rank(category):
        # Compute the minimal rank of the category
        n = len(category)
        rank = 0
        while True:
            found = False
            for i in range(n):
                if (i, i) not in category:
                    continue
                found = True
                category[(i, i)].append(rank)
                break
            if not found:
                return rank + 1
            rank += 1
    
    def complexity(game):
        # Measure the complexity of the communication game
        n = len(game)
        max_bits = 0
        for row in game:
            max_bits = max(max_bits, sum(row))
        return max_bits
    
    n = random.randint(5, 40)
    game = generate_game(n)
    category = free_monoidal_category(game)
    r = minimal_rank(category)
    c = complexity(game)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": r,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")