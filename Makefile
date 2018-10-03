default : ngp
ngp : main.c main.h payment_ethereum.c
	gcc main.c -o ngp
clean : 
	rm ngp