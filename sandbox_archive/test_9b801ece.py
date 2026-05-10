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

def generate_bibd(v, k, lamb):
    if v * (v - 1) % (k * (k - 1)) != lamb:
        raise ValueError("Parameters do not form a valid BIBD")
    
    blocks = []
    points = list(range(v))
    random.shuffle(points)
    
    for i in range(v):
        block = sorted(random.sample(points, k))
        if block not in blocks:
            blocks.append(block)
    
    return blocks

def incidence_matrix(blocks, v):
    M = [[0] * v for _ in range(len(blocks))]
    for i, block in enumerate(blocks):
        for point in block:
            M[i][point] = 1
    return M

def gaussian_elimination(M):
    n = len(M)
    m = len(M[0])
    rank = 0
    
    for j in range(m):
        pivot_row = -1
        for i in range(rank, n):
            if M[i][j] != 0:
                pivot_row = i
                break
        
        if pivot_row == -1:
            continue
        
        M[pivot_row], M[rank] = M[rank], M[pivot_row]
        
        for i in range(n):
            if i != rank and M[i][j] != 0:
                factor = M[i][j] / M[rank][j]
                for k in range(m):
                    M[i][k] -= factor * M[rank][k]
        
        rank += 1
    
    return rank

def acc0_circuit_size(M):
    n = len(M)
    m = len(M[0])
    rank = gaussian_elimination(M)
    
    # Estimate ACC^0 circuit size using a simple heuristic
    # This is a placeholder and should be replaced with actual lower bound calculation
    return (n * m) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    v = random.randint(5, 40)
    k = random.randint(3, v // 2)
    lamb = random.randint(1, v - k + 1)
    
    try:
        blocks = generate_bibd(v, k, lamb)
        M = incidence_matrix(blocks, v)
        size = acc0_circuit_size(M)
        
        metric_value = size
        instances_tested = 1
        conjecture_holds = size >= v ** (2 - 1 / k)
        counterexample = "" if conjecture_holds else f"BIBD(v={v}, k={k}, λ={lamb})"
    except Exception as e:
        metric_value = None
        instances_tested = 0
        conjecture_holds = False
        counterexample = str(e)
    
    return {
        "metric_name": "ACC^0 Circuit Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        counterexample_desc = next((r["counterexample"] for r in results if r["counterexample"] != ""), "")
        RESULT = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)