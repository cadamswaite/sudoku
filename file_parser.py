""" Program for getting grid,ans pairs from the tests dir """

def sudokus(qns="test/qns.txt", ans="test/ans.txt"):
    """ Returns (qn,ans) tuple generator """
    with open(qns) as fobj_qns, open(ans) as fobj_ans:
        for qn, an in zip(fobj_qns, fobj_ans):
            yield (qn.strip(), an.strip())


def test():
    """ Prints each puzzle, with its number"""
    for i, line in enumerate(sudokus()):
        print(f"Puzzle number {i}")
        print(line)

if __name__ == '__main__':
    test()
