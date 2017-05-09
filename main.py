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
                # if (eq[i] == 'X'):
                #     blk[2] = 1;
                blk[0].extend(eq[i]);
                blk[1] = '+';
            else:
                blk[1] = eq[i];
        else:
            if (eq[i] == 'X'):
                blk[2] = 1;
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
        # print("before : ");
        # print(blk[0]);
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
        blk[2] = exp;
        blk[0] = new_arr;
        # print(blk);

    # for blk in blks:
    #     indices = [i for i, x in enumerate(blk[0]) if x == 'X'];
    #     for i in indices:
    #         if (i + 2 <= len(blk[0])
    #             and blk[0][i + 1] == '^'
    #             and blk[0][i + 2] == '0'):
    #             del blk[0][i+1 : i+3];
    #             blk[0][i] = '1';
    #     if 'X' not in blk[0]:
    #         blk[2] = 0;

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
    res = 0;
    for blk in blks:
        mult = 1;
        for nb in ''.join(blk[0]).split("*"):
            mult *= int(nb);
        if blk[1] == '-':
            mult *= -1;
        res += mult;
    return res;

def printReducedForm(eq):
    print("Reduced form: ", end='');
    for i in range(0, len(eq[0])):
        print(eq[0][i][1] + ' ' + ''.join(eq[0][i][0]), end=' ');
    for i in range(0, len(eq[1])):
        print(('+' if eq[1][i][1] == '-' else '-') + ' ' + ''.join(eq[1][i][0]), end=' ');
    print("= 0");
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
        print(calc(eq[1]));
        print();
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
