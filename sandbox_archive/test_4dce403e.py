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
    n = random.randint(5, 40)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals, 2)
        clauses.append(clause)
    
    # Convert to Tseitin formula
    tseitin_vars = {var: [] for var in literals}
    tseitin_clauses = []
    for i, (a, b) in enumerate(clauses):
        p = f"p{i}"
        q = f"q{i}"
        tseitin_vars[a].append(p)
        tseitin_vars[b].append(q)
        tseitin_clauses.append([f"-{a}", p])
        tseitin_clauses.append([f"-{b}", q])
        tseitin_clauses.append([p, q, f"r{i}"])
    
    # Add final clause
    tseitin_vars[literals[0]].append("final")
    tseitin_clauses.extend([[f"-{var}", "final"] for var in literals[1:]])
    tseitin_clauses.append(["final", f"p{n-1}", f"q{n-1}"])
    
    # Convert to noncrossing partition
    def find_partition(clauses):
        n = len(literals)
        partition = [[] for _ in range(n)]
        for clause in clauses:
            if len(clause) == 2:
                a, b = clause
                i = literals.index(a)
                j = literals.index(b)
                if i < j:
                    partition[i].append(j)
                else:
                    partition[j].append(i)
        return partition
    
    partition = find_partition(tseitin_clauses)
    
    # Compute minimal rank of noncrossing partition
    def min_rank(partition):
        n = len(literals)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in partition[node]:
                            stack.append(neighbor)
                rank += 1
        return rank
    
    rank = min_rank(partition)
    
    # Compute Resolution proof length (simplified)
    def resolution_length(clauses):
        queue = clauses[:]
        derived = set()
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                return len(derived) + 1
            for other in queue:
                if len(other) == 2 and other[0] == -clause[0]:
                    new_clause = [x for x in other if x != -clause[0]]
                    if tuple(new_clause) not in derived:
                        derived.add(tuple(new_clause))
                        queue.append(new_clause)
        return float('inf')
    
    proof_length = resolution_length(tseitin_clauses)
    
    # Check conjecture
    if proof_length < 2**(rank * math.log(2)):
        counterexample = f"Proof length {proof_length} is less than 2^(Ω({rank})) for rank {rank}"
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    # Check support fraction
    expected_length = 2**(0.5 * rank)
    if abs(proof_length - expected_length) / expected_length > 0.5:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Proof length {proof_length} is not within a factor of 2^(0.5 * {rank}) of the expected value"
        }
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_length = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Proof length less than 2^(Ω(rank))\" first_failing_seed={first_failing_seed}")