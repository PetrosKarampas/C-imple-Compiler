#include <stdio.h>

int x, k, count, mult, T_1, T_2, T_3, T_4, T_5, T_6;

int main()
{
	L_1: count=0;  //(:=, 0, _, count)
	L_2: scanf("%d", &k);  //(inp, k, _, _)
	L_3: x=100;  //(:=, 100, _, x)
	L_4: if (k>1000) goto L_6;  //(>, k, 1000, 6)
	L_5: goto L_12;  //(jump, _, _, 12)
	L_6: T_1=count + 1;  //(+, count, 1, T_1)
	L_7: count=T_1;  //(:=, T_1, _, count)
	L_8: T_2=x * 30;  //(*, x, 30, T_2)
	L_9: x=T_2;  //(:=, T_2, _, x)
	L_10: k=69;  //(:=, 69, _, k)
	L_11: goto L_4;  //(jump, _, _, 4)
	L_12: if (k<500) goto L_14;  //(<, k, 500, 14)
	L_13: goto L_17;  //(jump, _, _, 17)
	L_14: T_3=x - 100;  //(-, x, 100, T_3)
	L_15: x=T_3;  //(:=, T_3, _, x)
	L_16: goto L_4;  //(jump, _, _, 4)
	L_17: T_4=x + 5;  //(+, x, 5, T_4)
	L_18: x=T_4;  //(:=, T_4, _, x)
	L_19: if (count==x) goto L_21;  //(=, count, x, 21)
	L_20: goto L_26;  //(jump, _, _, 26)
	L_21: T_5=mult * count;  //(*, mult, count, T_5)
	L_22: mult=T_5;  //(:=, T_5, _, mult)
	L_23: T_6=count + 10;  //(+, count, 10, T_6)
	L_24: count=T_6;  //(:=, T_6, _, count)
	L_25: goto L_19;  //(jump, _, _, 19)
	L_26: printf("%d", mult);  //(out, mult, _, _)

}