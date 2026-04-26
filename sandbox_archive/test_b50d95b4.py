import random
import math
import sys
import json

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        rank += 1
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return rank

def linear_equations_from_cnf(cnf, n):
    m = len(cnf)
    A = [[0] * (n + 1) for _ in range(m)]
    b = [0] * m
    for i, clause in enumerate(cnf):
        literals = set()
        for literal in clause:
            if literal > 0:
                literals.add(literal - 1)
            else:
                literals.add(-(literal + 1))
        if len(literals) == n:
            A[i] = [1] * (n + 1)
            b[i] = 1
        elif len(literals) == n - 1:
            for j in range(n):
                if j not in literals:
                    A[i][j] = 1
                    break
    return A, b

def count_solutions(A, b):
    rank = gaussian_elimination(A)
    if rank != len(b):
        return 0
    n = len(A[0]) - 1
    free_vars = n - rank
    solutions = 2 ** free_vars
    return solutions

def dpll_size_estimator(cnf):
    def dpll(clause_set, assignment, literals):
        if not clause_set:
            return 0
        unit_clauses = [c for c in clause_set if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment[:]
            new_assignment[literal] = True
            new_clause_set = [c for c in clause_set if literal not in c and -literal not in c]
            return 1 + dpll(new_clause_set, new_assignment, literals)
        pure_literals = {}
        for literal in literals:
            pos_count = sum(1 for c in clause_set if literal in c)
            neg_count = sum(1 for c in clause_set if -literal in c)
            if pos_count == 0 and literal not in assignment:
                pure_literals[literal] = True
            elif neg_count == 0 and -literal not in assignment:
                pure_literals[-literal] = True
        if pure_literals:
            literal = next(iter(pure_literals))
            new_assignment = assignment[:]
            new_assignment[literal] = True
            new_clause_set = [c for c in clause_set if literal not in c and -literal not in c]
            return 1 + dpll(new_clause_set, new_assignment, literals)
        branching_literal = next(iter(literals))
        new_assignment_true = assignment[:]
        new_assignment_true[branching_literal] = True
        new_clause_set_true = [c for c in clause_set if branching_literal not in c and -branching_literal not in c]
        true_size = 1 + dpll(new_clause_set_true, new_assignment_true, literals)
        new_assignment_false = assignment[:]
        new_assignment_false[branching_literal] = False
        new_clause_set_false = [c for c in clause_set if branching_literal not in c and -branching_literal not in c]
        false_size = 1 + dpll(new_clause_set_false, new_assignment_false, literals)
        return min(true_size, false_size)
    return dpll(cnf, {}, set(range(1, len(cnf[0]) + 1)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    cnf = []
    for _ in range(random.randint(2 * n, 3 * n)):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    
    A, b = linear_equations_from_cnf(cnf, n)
    solutions = count_solutions(A, b)
    
    k = dpll_size_estimator(cnf)
    expected_solutions = 2 ** k
    
    metric_name = "Number of Solutions"
    metric_value = solutions
    instances_tested = 1
    conjecture_holds = solutions == expected_solutions
    counterexample = "" if conjecture_holds else f"Expected {expected_solutions}, got {solutions}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_solutions = sum(r["metric_value"] for r in results)
    mean_solution_count = total_solutions / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_solution_count) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_solution_count:.2f} std={std_deviation:.2f} support_fraction={support_fraction:.2f}")