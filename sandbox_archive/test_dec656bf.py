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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def incidence_graph(clauses):
        graph = {i: set() for i in range(1, n + 1)}
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    graph[literal].add(-literal)
                else:
                    graph[-literal].add(literal)
        return graph
    
    def morse_complex(graph):
        rank = 0
        visited = set()
        stack = list(graph.keys())
        
        while stack:
            node = stack.pop()
            if node not in visited:
                rank += 1
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return rank
    
    n = random.randint(5, 40)
    clauses = generate_k_cnf(n)
    graph = incidence_graph(clauses)
    morse_rank = morse_complex(graph)
    
    if morse_rank > 10:
        counterexample = f"Rank {morse_rank} exceeds 10 for n={n}"
        return {
            "metric_name": "Morse Rank",
            "metric_value": morse_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    lower_bound = Fraction(2**(n/3)).limit_denominator()
    if morse_rank < lower_bound:
        return {
            "metric_name": "Morse Rank",
            "metric_value": morse_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {morse_rank} below lower bound {lower_bound} for n={n}"
        }
    
    return {
        "metric_name": "Morse Rank",
        "metric_value": morse_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_rank = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_rank = Fraction(total_rank).limit_denominator() / len(results)
    support_fraction = Fraction(count_conjecture_holds, len(results))
    
    print("RESULT:", "SUPPORTED" if support_fraction >= Fraction(4, 5) else "FALSIFIED", f"mean={mean_rank} std=unknown support_fraction={support_fraction}")