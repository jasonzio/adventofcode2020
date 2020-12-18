from typing import List, Dict


def infix_to_postfix(precedence: Dict[str, int], expression: str) -> List[str]:
    stack = []
    postfix = []
    for c in expression:
        if c == ' ':
            pass
        elif c in '0123456789':
            postfix.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while stack and precedence[c] <= precedence[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(c)
    while stack:
        postfix.append(stack.pop())
    return postfix


def eval_postfix(expression: List[str]) -> int:
    stack = []
    for token in expression:
        if token == '+':
            value = stack[-1] + stack[-2]
            stack.pop()
            stack[-1] = value
        elif token == '*':
            value = stack[-1] * stack[-2]
            stack.pop()
            stack[-1] = value
        else:
            stack.append(int(token))
    return stack[-1]


lines = open("input.txt").read().splitlines()
part1 = 0
part2 = 0
for line in lines:
    part1 += eval_postfix(infix_to_postfix({'+': 1, '*': 1, '(': 0}, line))
    part2 += eval_postfix(infix_to_postfix({'+': 2, '*': 1, '(': 0}, line))
print('part 1', part1)
print('part 2', part2)

