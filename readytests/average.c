#include <stdio.h>

int main()
{
int x, sum, average, T_1, T_2, T_3;

	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: sum=0;  //(:=, 0, _, sum)
	L_3: count=0;  //(:=, 0, _, count)
	L_4: if (x>1) goto L_6;  //(>, x, 1, 6)
	L_5: goto L_11;  //(jump, _, _, 11)
	L_6: T_1=sum + x;  //(+, sum, x, T_1)
	L_7: sum=T_1;  //(:=, T_1, _, sum)
	L_8: T_2=count + 1;  //(+, count, 1, T_2)
	L_9: count=T_2;  //(:=, T_2, _, count)
	L_10: goto L_4;  //(jump, _, _, 4)
	L_11: T_3=sum / count;  //(/, sum, count, T_3)
	L_12: average=T_3;  //(:=, T_3, _, average)
	L_13: printf('%d', average);  //(out, average, _, _)

}