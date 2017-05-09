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
                if (eq[i] == 'X'):
                    blk[2] = 1;
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


def cleanEqPow(eq):
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
        if (eq[1][i][2] == 1):
            eq[1][i][1] = '+' if eq[1][i][1] == '-' else '-';
            eq[0].append(eq[1][i]);
            eq[1].pop(i);
            pass;

def reduceForm(eq):
    if (len(eq) == 2):
        blks = [];
        eq[0] = splitInBlk(list(''.join(eq[0].split())));
        eq[1] = splitInBlk(list(''.join(eq[1].split())));

        cleanEqPow(eq);
        integersToTheRight(eq);

        simplifyEq(eq[0]);
        simplifyEq(eq[1]);

        for i in range(0, len(eq[0])):
            print(eq[0][i]);
        print("=");
        for i in range(0, len(eq[1])):
            print(eq[1][i]);

        print();
        print("Reduced form: ", end='');
        for i in range(0, len(eq[0])):
            print(eq[0][i][1] + ' ' + ''.join(eq[0][i][0]), end=' ');
        for i in range(0, len(eq[1])):
            print(('+' if eq[1][i][1] == '-' else '-') + ' ' + ''.join(eq[1][i][0]), end=' ');
        print("= 0");


    pass;

def argsToEq(args):
    eq = ''.join(args).split('=');
    return eq;

def main(argv):
    argv.pop(0);
    reduceForm(argsToEq(argv));
    pass;

if __name__ == "__main__":
    main(sys.argv);
