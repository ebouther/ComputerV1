import sys;

def splitInBlk(eq):
    blks = [];
    blk = [[], None, None];

    for i in range(0, len(eq)):
        #print("I :" + str(i) + " | " + str(eq[i]));
        if (eq[i] == '+'
                or eq[i] == '-'
                or i == 0):

            if (i != 0):
                #print("APPEND")
                blks.append(blk);
                blk = [[], None, None];

            if (eq[i] != '+' and eq[i] != '-'):
                blk[0].extend(eq[i]);
                #print("ADD : " + str(eq[i]));
                blk[1] = '+';
            else:
                blk[1] = eq[i];
                #print("BLK[1] : " + blk[1]);
        else:
            #print("ELSE");
            blk[0].extend(eq[i]);
    blks.append(blk);
    return blks;

def reduceForm(eq):
    if (len(eq) == 2):
        blks = [[], []];
        blks[0] = splitInBlk(eq[0].split());
        for i in range(0, len(blks[0])):
            print(blks[0][i]);
        print("---------");
        blks[1] = splitInBlk(eq[1].split());
        for i in range(0, len(blks[1])):
            print(blks[1][i]);



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
