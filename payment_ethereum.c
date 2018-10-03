#include <stdio.h>
#include <signal.h>

#include <cjson/cJSON.h>

#include "payment_ethereum.h"

T_PAYMENT_INTERFACE payment_ethereum_interface() {
  T_PAYMENT_INTERFACE interface;
  interface.payment_init = &payment_ethereum_init;
  interface.send_payment = &send_payment_ethereum;
  interface.payment_destroy = &payment_ethereum_destroy;
  return interface;
}

int payment_ethereum_init() {
  char *message = "POST / HTTP/1.0\r\nContent-Type: text/json\r\nContent-Length: 60\r\n\r\n{\"jsonrpc\":\"2.0\",\"method\":\"eth_accounts\",\"params\":[],\"id\":1}";

  struct hostent *server;
  struct sockaddr_in serv_addr;
  int sockfd, bytes, sent, received, total;
  char message[1024],response[4096];

  if (argc < 3) { puts("Parameters: <apikey> <command>"); exit(0); }

  /* fill in the parameters */
  sprintf(message,message_fmt,argv[1],argv[2]);
  printf("Request:\n%s\n",message);

  /* create the socket */
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) error("ERROR opening socket");

  /* lookup the ip address */
  server = gethostbyname(host);
  if (server == NULL) error("ERROR, no such host");

  /* fill in the structure */
  memset(&serv_addr,0,sizeof(serv_addr));
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(portno);
  memcpy(&serv_addr.sin_addr.s_addr,server->h_addr,server->h_length);

  /* connect the socket */
  if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0)
      error("ERROR connecting");

  /* send the request */
  total = strlen(message);
  sent = 0;
  do {
      bytes = write(sockfd,message+sent,total-sent);
      if (bytes < 0)
          error("ERROR writing message to socket");
      if (bytes == 0)
          break;
      sent+=bytes;
  } while (sent < total);

  /* receive the response */
  memset(response,0,sizeof(response));
  total = sizeof(response)-1;
  received = 0;
  do {
      bytes = read(sockfd,response+received,total-received);
      if (bytes < 0)
          error("ERROR reading response from socket");
      if (bytes == 0)
          break;
      received+=bytes;
  } while (received < total);

  if (received == total)
      error("ERROR storing complete response from socket");

  /* close the socket */
  close(sockfd);

  /* process response */
  printf("Response:\n%s\n",response);

  return 0;
}

void send_payment_ethereum(T_INTERFACE *interface, char *address, int64_t price) {
  char buffer[256];
  char *command = buffer;
  double price_double = price / 100000000.0f;
  sprintf(command, "electrum broadcast $(electrum payto %s %.8f -W password | jq -r '.hex')", address, price_double);
  printf("Sending bitoin payment with command %s\n",command);
  system(command);
}

void payment_ethereum_destroy(int pid_payment) {
  kill(pid_payment, SIGTERM);
}


