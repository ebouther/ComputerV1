# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ebouther <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/08 19:56:22 by ebouther          #+#    #+#              #
#    Updated: 2017/06/21 16:26:32 by ebouther         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys;
import os;
import re;


# blk = ["3 * 4", '+', 0]
# blk = ["3 * X * 4", '+', 1]
# blk = ["3 * X^2 * 4", '+', 2]

def my_abs(x):
    return x if x >= 0 else -x;

# Babylonian method
def sqrt(x):
    last_approx = x / 2.0;
    while True:
        approx = (last_approx + x / last_approx) / 2;
        if my_abs(approx - last_approx) < .00001:
            return approx;
        last_approx = approx;

def splitInBlk(eq):
    blks = [];
    blk = [[], None, 0];

    for i in range(0, len(eq)):
        if (((eq[i] == '+' or eq[i] == '-') and eq[i-1] != '^')
                or i == 0):

            if (i != 0):
                blks.append(blk);
                blk = [[], None, 0];

            if (eq[i] != '+' and eq[i] != '-'):
                blk[0].extend(eq[i]);
                blk[1] = '+';
            else:
                blk[1] = eq[i];
        else:
            blk[0].extend(eq[i]);
    blks.append(blk);
    return blks;

def simplifyEq(eq):
    for elem in eq:
        # pass value instead of reference
        inverse_elem = elem[:];
        inverse_elem[1] = '+' if inverse_elem[1] == '-' else '-';
        if inverse_elem in eq:
            eq.pop(eq.index(inverse_elem));
            eq.pop(eq.index(elem));
    pass;


def cleanEqPow(blks):
    for i in range(len(blks) - 1, -1, -1):
        new_arr = [];
        mult = 1;
        exp = 0;
        for nb in ''.join(blks[i][0]).split("*"):
            if (nb.find("X") > -1):
                if (len(nb) == 1):
                    exp += 1.0;
                else:
                    exp += float(nb[2:]);
            else:
                mult *= float(nb);
        if (mult != 1):
            if (mult == -1):
                blks[i][1] = '+' if blks[i][1] == '-' else '-';
            else:
                if (len(new_arr) > 0):
                    new_arr.extend(['*']);
                new_arr.extend(str(mult));
        if len(new_arr) == 0:
            new_arr.extend('1');
        if (mult == 0):
            blks.pop(i);
        else:
            blks[i][2] = exp;
            if (exp > 2):
                print("\033[31mPolynomial degree: {}\033[0m\n".format(exp));
                print('Only solves degree 2 or less polynomials\n');
                os._exit(1)
            blks[i][0] = new_arr;
    pass;

# Return neg as long as X with negative exp are found.
def negative_pow(eq):
    neg = 0;
    for i in range(len(eq[0])):
        if (eq[0][i][1] < 0):
            neg = 1;
            deg = eq[0][i][1] * -1;
            eq[0][i][1] = 0;
            for n in range(len(eq[0])):
                if (n != i):
                    eq[0][n][1] += deg;
            for n in range(len(eq[1])):
                eq[1][n][1] += deg;
    return neg;

def integersToTheRight(eq):
    #iterate backward enables to pop elements while looping
    for i in range(len(eq[0]) - 1, -1, -1):
        if (eq[0][i][1] == 0):
            eq[0][i][0] *= -1;
            eq[1].append(eq[0][i]);
            eq[0].pop(i);
    # Unknown to the left
    for i in range(len(eq[1]) - 1, -1, -1):
        if (eq[1][i][1] != 0):
            eq[1][i][0] *= -1;
            eq[0].append(eq[1][i]);
            eq[1].pop(i);
    pass;

# Merge blocks with same degree and change replace strings with float.
# Ex: [["5.0", '+', 1.0] ["7.0", '-', 1.0]] => [[-2.0, 1.0]]
def calc(blks):
    values = set(map(lambda x:x[2], blks));
    sortByDegree = [[y[:] for y in blks if y[2]==x] for x in values];

    blks = [];
    for blocks in sortByDegree:
        res = 0;
        for blk in blocks:
            if blk[1] == '-':
                res += float(''.join(blk[0])) * -1;
            else:
                res += float(''.join(blk[0]));
        if (res != 0):
            blks.append([res, blocks[0][2]]);
    return blks;

# does the same as calc() after the blocks were epured (case of X with negative exponent)
def recalc(blks):
    values = set(map(lambda x:x[1], blks));
    sortByDegree = [[y[:] for y in blks if y[1]==x] for x in values];

    blks = [];
    for blocks in sortByDegree:
        res = 0;
        for blk in blocks:
            res += blk[0];
        if (res != 0):
            blks.append([res, blocks[0][1]]);
    return blks;


def printEq(eq):
    print("\033[36m\t       => ", end='');
    for i in range(0, len(eq[0])):
        if (i != 0 and eq[0][i][0] >= 0):
            print("+", end=' ');
        print(eq[0][i][0], end=' ');
        if eq[0][i][1] != 0:
            print("* X^{}".format(eq[0][i][1]), end=' ');
    print(" = ", end="");
    print(str(eq[1][0][0]), end=' ');
    print("\033[0m\n");
    pass;

def printReducedForm(eq):
    print("\n\033[36mReduced form: ", end='');
    for i in range(0, len(eq[0])):
        print((eq[0][i][1] if not (i == 0 and eq[0][i][1] == '+') else '') + ' ' + ''.join(eq[0][i][0]), end=' ');
        if eq[0][i][2] != 0:
            print("* X^{}".format(eq[0][i][2]), end=' ');
    for i in range(0, len(eq[1])):
        print(('+' if eq[1][i][1] == '-' else '-') + ' ' + ''.join(eq[1][i][0]), end=' ');
    if (len(eq[0]) == 0 and len(eq[1]) == 0):
        print("0 ", end = '');
    print("= 0\033[0m\n");
    pass;


def solveQuadratic(eq):

    print("\033[31mPolynomial degree: 2\033[0m\n");

    a = 0;
    b = 0;
    c = eq[1][0][0] * -1;

    for blk in eq[0]:
        if blk[1] == 2:
            a = blk[0];
        elif blk[1] == 1:
            b = blk[0];

    print("a: {}".format(a));
    print("b: {}".format(b));
    print("c: {}\n".format(c));

    delta = (b * b) - (4 * a * c);
    print("𝚫 = b² - 4ac");
    print("𝚫 = ({})² - 4 * ({}) * ({})".format(b, a, c));
    print("𝚫 = {}\n\033[36m".format(delta));

    if delta > 0:
        print("𝚫 > 0");
        print("Two solutions:");
        print("X0 = (-b - sqrt(𝚫)) / 2a");
        print("X0 = (-({}) - sqrt({})) / (2 * ({}))".format(b, delta, a));

        print("X1 = (-b + sqrt(𝚫)) / 2a");
        print("X1 = (-({}) + sqrt({})) / (2 * ({}))".format(b, delta, a));
        sol1 = ((-b) - sqrt(delta)) / (2 * a);
        sol2 = ((-b) + sqrt(delta)) / (2 * a);
        print("\033[32m\tX0 = {:.5f}".format(sol1));
        print("\tX1 = {:.5f}\033[0m".format(sol2));
    elif delta == 0:
        print("𝚫 = 0");
        print("1 solution:");
        print("X = -b / 2a");
        print("X = -({}) / (2 * ({}))".format(b, a));
        sol1 = (-b) / (2 * a);
        print("\t\033[32mX = {}\033[0m".format(sol1));
    else:
        print("𝚫 < 0");
        print("No real solution.");
        print("2 complex solutions :");

        print("R X0 = -b / 2a");
        print("R X0 = -({}) / (2 * ({}))".format(b, a));
        print("I X0 = sqrt(-𝚫) / 2a)".format(delta, a));
        print("I X0 = sqrt(-({})) / (2 * ({}))\n".format(delta, a));

        print("R X1 = -b / 2a");
        print("R X1 = -({}) / (2 * ({}))".format(b, a));
        print("I X1 = -sqrt(-𝚫) / 2a)".format(delta, a));
        print("I X1 = -sqrt(-({})) / (2 * ({}))\n".format(delta, a));

        real = -b / (2 * a);
        imaginary = sqrt(-delta) / (2 * a);
        print("\t\033[32mX0 = {:.5f} + {:.5f}i".format(real, imaginary));

        imaginary = -sqrt(-delta) / (2 * a);
        print("\tX1 = {:.5f} + {:.5f}i\033[0m".format(real, imaginary));
    pass;

def solveAffine(eq):
    print("\033[31mPolynomial degree: 1\033[0m\n");
    if (eq[0][0][0] < 0 and eq[1][0][0] < 0):
        print("\033[32m\tX = {} / {}\033[0m".format(-eq[1][0][0], -eq[0][0][0]));
    else:
        print("\033[32m\tX = {} / {}\033[0m".format(eq[1][0][0], eq[0][0][0]));
    print("\033[32m\tX = {:.5f}\033[0m".format(eq[1][0][0] / eq[0][0][0]));
    pass;

def solveEq(eq):
    if (len(eq) == 2):
        blks = [];
        eq[0] = splitInBlk(list(''.join(eq[0].split())));
        eq[1] = splitInBlk(list(''.join(eq[1].split())));

        #print ("EQ : {}".format(eq));

        cleanEqPow(eq[0]);
        cleanEqPow(eq[1]);

        #print ("EQ : {}".format(eq));

        simplifyEq(eq[0]);
        simplifyEq(eq[1]);

        #print ("EQ : {}".format(eq));
        printReducedForm(eq);

        eq[0] = calc(eq[0]);
        eq[1] = calc(eq[1]);

        #print ("EQ : {}".format(eq));

        ret = 1;
        while (ret):
            ret = negative_pow(eq);
            integersToTheRight(eq);
            eq[0] = recalc(eq[0]);
            eq[1] = recalc(eq[1]);

        #print ("EQ : {}".format(eq));

        if not (len(eq[1])):
           eq[1] = [[0, 0]];
        if (len(eq[0])):
            printEq(eq);

        max_degree = 0;
        for blk in eq[0]:
            if (max_degree < blk[1]):
                max_degree = blk[1];
        if max_degree == 1:
            solveAffine(eq);
        elif max_degree == 2:
            solveQuadratic(eq);
        elif max_degree > 2:
            print("\033[31mPolynomial degree: {}\033[0m\n".format(max_degree));
            print('Only solves degree 2 or less polynomials\n');
        elif len(eq[0]) == 0 and len(eq[1]) == 0:
            print("True for all X");
        else:
            print("No solution");
    else:
        print("Bad input.")
    pass;

def main(argv):
    if (len(argv) == 2):
        reg=re.compile('^[0-9 X\+\-\.\=\^\*\t\n]+$');
        if (reg.match(argv[1])):
            try:
               solveEq(argv[1].split('='));
            except:
                print("Bad input.");
                os._exit(1);
        else:
            print("Bad input.")
    else:
        print("Please pass equation as argument.")
    pass;

if __name__ == "__main__":
    main(sys.argv);
