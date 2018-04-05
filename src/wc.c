#define YES 1
#define NO 0
#define EOF 2

int main()
{
    int c, nw, inword ;
    inword = NO ;
    nw = 0;
    c = getchar();
    while ( c != EOF ) {
        if ( c == ' ' || c == '\n' || c == '\t')
            inword = NO;
        else if (inword == NO) {
            inword = YES ;
            nw = nw + 1;
        }
        c = getchar();
    }
    printf("%d \n",nw);
}
