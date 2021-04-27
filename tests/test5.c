#include <stdio.h>

int x, y, z, b, f, g, T_1, T_2, T_3;

int main()
{
	L_1: scanf("%d", &x);  //(inp, x, _, _)
	L_2: y=2;  //(:=, 2, _, y)
	L_3: scanf("%d", &b);  //(inp, b, _, _)
	L_4: f=y;  //(:=, y, _, f)
	L_5: g=10;  //(:=, 10, _, g)
	L_6: if (b>1) goto L_14;  //(>, b, 1, 14)
	L_7: goto L_8;  //(jump, _, _, 8)
	L_8: if (f<2) goto L_14;  //(<, f, 2, 14)
	L_9: goto L_10;  //(jump, _, _, 10)
	L_10: T_1=g + 1;  //(+, g, 1, T_1)
	L_11: T_2=f + b;  //(+, f, b, T_2)
	L_12: if (T_1<T_2) goto L_24;  //(<, T_1, T_2, 24)
	L_13: goto L_14;  //(jump, _, _, 14)
	L_14: if (b>=10) goto L_16;  //(>=, b, 10, 16)
	L_15: goto L_23;  //(jump, _, _, 23)
	L_16: T_3=b - 10;  //(-, b, 10, T_3)
	L_17: b=T_3;  //(:=, T_3, _, b)
	L_18: if (f>2) goto L_20;  //(>, f, 2, 20)
	L_19: goto L_22;  //(jump, _, _, 22)
	L_20: printf("%d\n", f);  //(out, f, _, _)
	L_21: goto L_22;  //(jump, _, _, 22)
	L_22: goto L_14;  //(jump, _, _, 14)
	L_23: goto L_26;  //(jump, _, _, 26)
	L_24: scanf("%d", &g);  //(inp, g, _, _)
	L_25: printf("%d\n", g);  //(out, g, _, _)
	L_26: {}  //(halt, _, _, _)
}