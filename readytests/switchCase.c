#include <stdio.h>

int x, y, T_1, T_2, T_3, T_4, T_5;

int main()
{
	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: if (y<=0) goto L_4;  //(<=, y, 0, 4)
	L_3: goto L_7;  //(jump, _, _, 7)
	L_4: T_1=x * 2;  //(*, x, 2, T_1)
	L_5: y=T_1;  //(:=, T_1, _, y)
	L_6: goto L_21;  //(jump, _, _, 21)
	L_7: if (x>0) goto L_9;  //(>, x, 0, 9)
	L_8: goto L_14;  //(jump, _, _, 14)
	L_9: T_2=y * 3;  //(*, y, 3, T_2)
	L_10: printf('%d', T_2);  //(out, T_2, _, _)
	L_11: T_3=x * 2;  //(*, x, 2, T_3)
	L_12: y=T_3;  //(:=, T_3, _, y)
	L_13: goto L_21;  //(jump, _, _, 21)
	L_14: if (y==2) goto L_16;  //(=, y, 2, 16)
	L_15: goto L_19;  //(jump, _, _, 19)
	L_16: T_4=x + y;  //(+, x, y, T_4)
	L_17: printf('%d', T_4);  //(out, T_4, _, _)
	L_18: goto L_21;  //(jump, _, _, 21)
	L_19: T_5=x * 2;  //(*, x, 2, T_5)
	L_20: return T_5;  //(retv, T_5, _, _)
	L_21: return x;  //(retv, x, _, _)

}