from src.util import parse_problem
from src.chromosome import Chromosome

if __name__ == '__main__':
    problem = parse_problem("../data/problem/p01")
    c = Chromosome(problem)