#include <stdio.h>

int main()
{
int x, count, T_1, T_2;

	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: count=0;  //(:=, 0, _, count)
	L_3: if (x>0) goto L_5;  //(>, x, 0, 5)
	L_4: goto L_10;  //(jump, _, _, 10)
	L_5: T_1=x / 10;  //(/, x, 10, T_1)
	L_6: x=T_1;  //(:=, T_1, _, x)
	L_7: T_2=count + 1;  //(+, count, 1, T_2)
	L_8: count=T_2;  //(:=, T_2, _, count)
	L_9: goto L_3;  //(jump, _, _, 3)
	L_10: printf('%d', count);  //(out, count, _, _)

}