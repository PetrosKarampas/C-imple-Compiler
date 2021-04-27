#include <stdio.h>

int main()
{
int x, sum, T_1;

	L_1: scanf('%d', &x);  //(inp, x, _, _)
	L_2: sum=0;  //(:=, 0, _, sum)
	L_3: if (x>0) goto L_5;  //(>, x, 0, 5)
	L_4: goto L_8;  //(jump, _, _, 8)
	L_5: T_1=sum + x;  //(+, sum, x, T_1)
	L_6: sum=T_1;  //(:=, T_1, _, sum)
	L_7: goto L_3;  //(jump, _, _, 3)
	L_8: printf('%d', sum);  //(out, sum, _, _)

}