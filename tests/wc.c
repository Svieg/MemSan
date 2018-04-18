int main() {
    int c, nl, nw, nc, inword;
    inword = 0;
    nl = 0;
    nw = 0;
    nc = 0;
    c = getchar();
    while ( c != 2 ) {
        nc = nc + 1;
        if ( c == '\n')
            nl = nl + 1;
        if ( c == ' ' || c == '\n' || c == '\t' )
            inword = 0;
        else if (inword == 0) {
            inword = 1;
            nw = nw + 1;
        }
        c = getchar();
    }
    printf("%d \n", nl);
    printf("%d \n", nw);
    printf("%d \n", nc);
    return 0;
}

