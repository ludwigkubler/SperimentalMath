import random
import math
import sys
import json
from collections import defaultdict

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                for j in range(cols):
                    matrix[k][j] -= matrix[i][j] * matrix[k][i]
    rank = sum(1 for row in matrix if any(row))
    return rank

def generate_cnf_tautology(n, m):
    variables = list(range(n))
    clauses = []
    while len(clauses) < m:
        clause = random.sample(variables + [-v for v in variables], n)
        if all(v not in c and -v not in c for c in clauses):
            clauses.append(clause)
    return clauses

def dpll_solve(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    free_vars = [v for v in range(1, max(cnf) + 1) if v not in assignment and -v not in assignment]
    if not free_vars:
        return all(all(lit in assignment and assignment[lit] for lit in clause) or any(-lit in assignment and not assignment[-lit] for lit in clause) for clause in cnf)
    var = free_vars[0]
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var if val else -var] = True
        if dpll_solve(cnf, new_assignment):
            return True
    return False

def extended_frege_size(cnf):
    if len(cnf) == 0:
        return 1
    max_clause_length = max(len(clause) for clause in cnf)
    proof_size = max_clause_length + 1
    for _ in range(10):  # Simple heuristic to estimate proof size
        new_clause = [random.choice([-v, v] for v in range(1, max(cnf) + 1)) for _ in range(max_clause_length)]
        if dpll_solve(cnf + [new_clause]):
            proof_size += 1
    return proof_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    m = 2 * n
    cnf = generate_cnf_tautology(n, m)
    
    incidence_matrix = [[int(v in clause or -v in clause) for v in range(1, n + 1)] for clause in cnf]
    matroid_rank = gaussian_elimination(incidence_matrix)
    
    proof_size = extended_frege_size(cnf)
    
    conjecture_holds = (matroid_rank >= 2**(n/2)) == (proof_size > 10**6)  # Super-polynomial size is greater than 1e6
    counterexample = "" if conjecture_holds else f"Matroid rank: {matroid_rank}, Proof size: {proof_size}"
    
    return {
        "metric_name": "Extended Frege proof size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append((result["metric_value"], result["conjecture_holds"]))
    
    mean_metric_value = sum(v for v, _ in results) / len(results)
    std_metric_value = math.sqrt(sum((v - mean_metric_value)**2 for v, _ in results) / len(results))
    support_fraction = sum(holds for _, holds in results) / len(results)
    
    if all(holds for _, holds in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not holds for _, holds in results):
        first_failing_seed = seeds[next(i for i, (_, holds) in enumerate(results) if not holds)]
        print(f"RESULT: FALSIFIED counterexample=\"Matroid rank and proof size do not correlate\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")