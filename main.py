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


def reduceForm(eq):
    if (len(eq) == 2):
        blks = [];
        left_part = splitInBlk(list(''.join(eq[0].split())));
        right_part = splitInBlk(list(''.join(eq[1].split())));

        # inverse right part
        for i in range(0, len(right_part)):
            right_part[i][1] = '+' if right_part[i][1] == '-' else '-';
        left_part.extend(right_part);
        for i in range(0, len(left_part)):
            print(left_part[i]);

        # Simplify equation
        for elem in left_part:
            # pass value instead of reference
            inverse_elem = elem[:];
            inverse_elem[1] = '+' if inverse_elem[1] == '-' else '-';
            if inverse_elem in left_part:
                left_part.pop(left_part.index(inverse_elem));
                left_part.pop(left_part.index(elem));
        print();
        print("Reduced form: ", end='');
        for i in range(0, len(left_part)):
            print(left_part[i][1] + ' ' + ''.join(left_part[i][0]), end=' ');
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
