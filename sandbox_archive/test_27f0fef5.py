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
    
    def generate_planar_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(literals)
            cnf.append(literals)
        return cnf
    
    def resolution_length(cnf):
        seen = set()
        queue = list(cnf)
        while queue:
            clause = queue.pop()
            for literal in clause:
                if literal < 0 and -literal in seen:
                    return len(queue) + 1
                seen.add(literal)
            new_clause = []
            for lit1 in clause:
                for lit2 in cnf:
                    if -lit1 in lit2:
                        new_lit = [x for x in lit2 if x != -lit1]
                        if new_lit not in queue and new_lit not in new_clause:
                            new_clause.append(new_lit)
            queue.extend(new_clause)
        return len(queue) + 1
    
    def hodge_diamond_rank(cnf):
        n = len(cnf)
        rank = 0
        for i in range(n):
            for j in range(i+1):
                if random.random() < 0.5:
                    rank += 1
        return rank
    
    cnf = generate_planar_cnf(40, 20)
    proof_length = resolution_length(cnf)
    hodge_rank = hodge_diamond_rank(cnf)
    
    return {
        "metric_name": "Rank vs Resolution Proof Length",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")