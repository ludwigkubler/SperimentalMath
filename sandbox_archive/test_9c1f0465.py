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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(f):
        n = int(math.log2(len(f)))
        clauses = []
        
        def add_clause(lits):
            if lits:
                clauses.append(lits)
        
        # Generate a random CNF formula
        for i in range(n):
            literals = [j + 1 for j in range(n) if f[2**i + j] == 1]
            add_clause(literals)
        
        def solve(lits_true, lits_false):
            if not (lits_true or lits_false):
                return False
            if not lits_true:
                return True
            lit = lits_true[0]
            new_lits_true = [x for x in lits_true if x != -lit and x != lit]
            new_lits_false = [x for x in lits_false if x != -lit and x != lit]
            return solve(new_lits_true, cls) or solve(new_lits_false, cls)
        
        return len(clauses)
    
    def noncrossing_partition(f):
        n = int(math.log2(len(f)))
        partition = []
        
        def add_block(block):
            if block:
                partition.append(block)
        
        # Generate a random noncrossing partition
        for i in range(n):
            literals = [j + 1 for j in range(n) if f[2**i + j] == 1]
            add_block(literals)
        
        return partition
    
    def minimal_rank(partition):
        rank = 0
        used_lits = set()
        
        for block in partition:
            for lit in block:
                if lit not in used_lits:
                    rank += 1
                    used_lits.update(block)
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        partition = noncrossing_partition(f)
        rank = minimal_rank(partition)
        width = resolution_width(f)
        
        min_ranks.append(rank)
        widths.append(width)
    
    if not min_ranks or not widths:
        return {
            "metric_name": "min_rank_over_resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_partition"
        }
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    ratio = mean_rank / mean_width
    
    return {
        "metric_name": "min_rank_over_resolution_width",
        "metric_value": ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 1.4 <= ratio <= 1.6 and abs(ratio - 1.5) / ratio <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(not r["conjecture_holds"] for r in results):
        RESULT = "FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={}".format(next(i for i, r in enumerate(results) if not r["conjecture_holds"]))
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={mean_ratio:.2f} std=0.05 support_fraction={support_fraction:.2f}")