#include <stdio.h>

#define PAYMENT_INTERFACE_ETHEREUM_IDENTIFIER 3

#define ETHEREUM_ADDRESS_LEN 36

#ifndef PAYMENT_ETHEREUM_H

#define PAYMENT_ETHEREUM_H

T_PAYMENT_INTERFACE payment_ethereum_interface();

int payment_ethereum_init();

void send_payment_ethereum(T_INTERFACE *interface, char *address, int64_t price);

void payment_ethereum_destroy(int pid_payment);

#endif
