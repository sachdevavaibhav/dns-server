import socket  # socket module is used to create a socket object that can communicate with other machines. Socket is basically an endpoint that handles communication between machines and processes. It is a combination of IP address and port number.
from app.utils.message import DnsMessage
from app.logger import log
from argparse import ArgumentParser


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    log.info("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    parser = ArgumentParser()
    parser.add_argument("--resolver", type=str)
    args = parser.parse_args()
    log.debug(f"Args: {args}")

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            log.debug(buf)
            message = DnsMessage(buf)

            if args.resolver:
                message.forward(args.resolver)
            else:
                message.add_answer()

            response = message.respond()
            # log.debug(response)
            udp_socket.sendto(response, source)
        except Exception as e:
            log.error(f"Error receiving data: {e}", exc_info=True)
            break


if __name__ == "__main__":
    main()
