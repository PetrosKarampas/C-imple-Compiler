#include <stdio.h>

int main()
{
int x, i, fact, T_1, T_2;

	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: fact=1;  //(:=, 1, _, fact)
	L_3: i=1;  //(:=, 1, _, i)
	L_4: if (i<=x) goto L_6;  //(<=, i, x, 6)
	L_5: goto L_11;  //(jump, _, _, 11)
	L_6: T_1=fact * i;  //(*, fact, i, T_1)
	L_7: fact=T_1;  //(:=, T_1, _, fact)
	L_8: T_2=i + 1;  //(+, i, 1, T_2)
	L_9: i=T_2;  //(:=, T_2, _, i)
	L_10: goto L_4;  //(jump, _, _, 4)
	L_11: printf('%d', fact);  //(out, fact, _, _)

}