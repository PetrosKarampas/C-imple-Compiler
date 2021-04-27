#include <stdio.h>

int n1, n2, T_1, T_2;

int main()
{
	L_1: scanf("%d", &n1);  //(inp, n1, _, _)
	L_2: scanf("%d", &n2);  //(inp, n2, _, _)
	L_3: if (n1!=n2) goto L_5;  //(<>, n1, n2, 5)
	L_4: goto L_13;  //(jump, _, _, 13)
	L_5: if (n1>n2) goto L_7;  //(>, n1, n2, 7)
	L_6: goto L_10;  //(jump, _, _, 10)
	L_7: T_1=n1 - n2;  //(-, n1, n2, T_1)
	L_8: n1=T_1;  //(:=, T_1, _, n1)
	L_9: goto L_12;  //(jump, _, _, 12)
	L_10: T_2=n2 - n1;  //(-, n2, n1, T_2)
	L_11: n2=T_2;  //(:=, T_2, _, n2)
	L_12: goto L_3;  //(jump, _, _, 3)
	L_13: printf("%d", n1);  //(out, n1, _, _)

}