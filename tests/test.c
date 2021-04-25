#include <stdio.h>

int x, i, fact, T_1, T_2;

int main()
{
	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: fact=1;  //(:=, 1, _, fact)
	L_3: i=1;  //(:=, 1, _, i)
	L_4: if (i<=x) goto L_6;  //(<=, i, x, 6)
	L_5: goto L_13;  //(jump, _, _, 13)
	L_6: if (fact!=19) goto L_13;  //(<>, fact, 19, 13)
	L_7: goto L_8;  //(jump, _, _, 8)
	L_8: if (x<2) goto L_13;  //(<, x, 2, 13)
	L_9: goto L_10;  //(jump, _, _, 10)
	L_10: T_1=fact + 1;  //(+, fact, 1, T_1)
	L_11: i=T_1;  //(:=, T_1, _, i)
	L_12: goto L_15;  //(jump, _, _, 15)
	L_13: T_2=x - 1;  //(-, x, 1, T_2)
	L_14: x=T_2;  //(:=, T_2, _, x)

}