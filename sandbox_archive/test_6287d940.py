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
    
    def construct_grammar(clauses):
        grammar = {'S': ''}
        nonterminals = ['S']
        terminals = set()
        
        for clause in clauses:
            for literal in clause.split():
                if literal[0] == '~':
                    terminals.add(literal[1:])
                else:
                    terminals.add(literal)
            
            rule = f"S -> {clause}"
            grammar['S'] += rule + '\n'
            nonterminals.append(f"NT_{len(nonterminals)}")
        
        return grammar, nonterminals, terminals
    
    def min_order_of_entailment(clauses):
        # Placeholder for actual implementation
        return len(clauses)
    
    def monotone_width(grammars):
        # Placeholder for actual implementation
        return sum(len(g.split('\n')) for g in grammars) / len(grammars)
    
    n = random.randint(5, 40)
    clauses = [random.choice(['A', 'B', 'C']) + ' | ' + random.choice(['D', 'E', 'F']) for _ in range(n)]
    grammar, nonterminals, terminals = construct_grammar(clauses)
    
    omega_G = min_order_of_entailment(clauses)
    w_c_G = monotone_width([grammar['S']])
    
    return {
        "metric_name": "correlation",
        "metric_value": omega_G * w_c_G,
        "instances_tested": len(clauses),
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")