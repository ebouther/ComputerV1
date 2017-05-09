import sys;

def splitInBlk(eq):
    blks = [];
    blk = [[], None, 0];

    for i in range(0, len(eq)):
        if (eq[i] == '+'
                or eq[i] == '-'
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

#Got to improve when 3 * X and X * 3
#               when 4 * 3 and 3 * 4
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

    for blk in blks:
        new_arr = [];
        mult = 1;
        exp = 0;
        for nb in ''.join(blk[0]).split("*"):
            if (nb.find("X") > -1): # should set degree here.
                exp += int(nb[2:]);
            else:
                mult *= int(nb);
        if (mult != 1):
            if (mult == -1):
                blk[1] = '+' if blk[1] == '-' else '-';
            else:
                if (len(new_arr) > 0):
                    new_arr.extend(['*']);
                new_arr.extend(str(mult));
        if len(new_arr) == 0:
            new_arr.extend('1');
        blk[2] = exp;
        if (exp > 2):
            raise ValueError('Only solve degree 2 or less polynomials');
        blk[0] = new_arr;
    pass;

def integersToTheRight(eq):
    #iterate backward enables to pop elements while looping
    for i in range(len(eq[0]) - 1, -1, -1):
        if (eq[0][i][2] == 0):
            eq[0][i][1] = '+' if eq[0][i][1] == '-' else '-';
            eq[1].append(eq[0][i]);
            eq[0].pop(i);
    # Unknown to the left
    for i in range(len(eq[1]) - 1, -1, -1):
        if (eq[1][i][2] > 0):
            eq[1][i][1] = '+' if eq[1][i][1] == '-' else '-';
            eq[0].append(eq[1][i]);
            eq[1].pop(i);
    pass;

def calc(blks):

    values = set(map(lambda x:x[2], blks));
    sortByDegree = [[y[:] for y in blks if y[2]==x] for x in values];

    blks = [];
    for blocks in sortByDegree:
        res = 0;
        for blk in blocks:
            if blk[1] == '-':
                res += int(''.join(blk[0])) * -1;
            else:
                res += int(''.join(blk[0]));
        print("RES : " + str(res) + " | exp : " + str(blocks[0][2]));
        if (blocks[0][2] == 0):
            blks.append(res);
        else:
            blks.append([res, blocks[0][2]]);
    return blks;

def printReducedForm(eq):
    print("Reduced form: ", end='');
    for i in range(0, len(eq[0])):
        print(eq[0][i][1] + ' ' + ''.join(eq[0][i][0]), end=' ');
    for i in range(0, len(eq[1])):
        print(('+' if eq[1][i][1] == '-' else '-') + ' ' + ''.join(eq[1][i][0]), end=' ');
    print("= 0");
    pass;


def solveAffine(eq):

    print("X = ", end='');
    print(eq[1][0] / eq[0][0][0]);
    pass;

def solveEq(eq):
    if (len(eq) == 2):
        blks = [];
        eq[0] = splitInBlk(list(''.join(eq[0].split())));
        eq[1] = splitInBlk(list(''.join(eq[1].split())));

        cleanEqPow(eq[0]);
        cleanEqPow(eq[1]);

        integersToTheRight(eq);

        simplifyEq(eq[0]);
        simplifyEq(eq[1]);

        print();
        printReducedForm(eq);

        print ("\n=======");
        for i in range(0, len(eq[0])):
            print(eq[0][i], end='');
        print(" = ", end='');
        for i in range(0, len(eq[1])):
            print(eq[1][i], end='');

        eq[0] = calc(eq[0]);
        eq[1] = calc(eq[1]);

        print ("\n=======");
        for i in range(0, len(eq[0])):
            print(eq[0][i], end='');
        print(" = ", end='');
        for i in range(0, len(eq[1])):
            print(eq[1][i], end='');
        print();

        if len(eq[0]) == 1 and eq[0][0][1] == 1: # if affine
            solveAffine(eq);
    pass;

def argsToEq(args):
    eq = ''.join(args).split('=');
    return eq;

def main(argv):
    argv.pop(0);
    solveEq(argsToEq(argv));
    pass;

if __name__ == "__main__":
    main(sys.argv);
