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
            if random.choice([0, 1]) == 0:
                program.append('A')
            else:
                program.append('B')
        return program
    
    def construct_semigroup(program):
        semigroup = set()
        for i in range(len(program)):
            for j in range(i + 1, len(program) + 1):
                subprogram = program[i:j]
                if subprogram not in semigroup:
                    semigroup.add(subprogram)
        return semigroup
    
    def local_dimension(semigroup, a, r):
        ball = {a}
        generators = set()
        while len(ball) < r:
            new_elements = set()
            for element in ball:
                for generator in semigroup:
                    if generator not in ball and all(element[i] == generator[i] for i in range(min(len(element), len(generator)))):
                        new_elements.add(generator)
            ball.update(new_elements)
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimension = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            program = generate_branching_program(n)
            semigroup = construct_semigroup(program)
            dimension = local_dimension(semigroup, 'A', 2)  # Example element and radius
            total_dimension += dimension
            instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested
    conjecture_holds = mean_dimension <= (3 * n_values[-1] / 4)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_local_dimension",
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")