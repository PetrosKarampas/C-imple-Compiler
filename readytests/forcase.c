#include <stdio.h>

int main()
{
int x, count, mult, T_1, T_2, T_3, T_4, T_5;

	L_1: if (k>1000) goto L_3;  //(>, k, 1000, 3)
	L_2: goto L_6;  //(jump, _, _, 6)
	L_3: T_1=t * 30;  //(*, t, 30, T_1)
	L_4: t=T_1;  //(:=, T_1, _, t)
	L_5: goto L_1;  //(jump, _, _, 1)
	L_6: if (k<500) goto L_8;  //(<, k, 500, 8)
	L_7: goto L_11;  //(jump, _, _, 11)
	L_8: T_2=t - 100;  //(-, t, 100, T_2)
	L_9: t=T_2;  //(:=, T_2, _, t)
	L_10: goto L_1;  //(jump, _, _, 1)
	L_11: T_3=t + 5;  //(+, t, 5, T_3)
	L_12: t=T_3;  //(:=, T_3, _, t)
	L_13: if (count<=y) goto L_15;  //(<=, count, y, 15)
	L_14: goto L_20;  //(jump, _, _, 20)
	L_15: T_4=mult * count;  //(*, mult, count, T_4)
	L_16: mult=T_4;  //(:=, T_4, _, mult)
	L_17: T_5=count + 10;  //(+, count, 10, T_5)
	L_18: count=T_5;  //(:=, T_5, _, count)
	L_19: goto L_13;  //(jump, _, _, 13)
	L_20: printf('%d', mult);  //(out, mult, _, _)

}