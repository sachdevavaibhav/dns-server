import socket  # socket module is used to create a socket object that can communicate with other machines. Socket is basically an endpoint that handles communication between machines and processes. It is a combination of IP address and port number.
from app.utils.header import (
    DnsHeader,
)
from app.utils.question import Question
from app.utils.answer import Answer


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            buf_data = DnsHeader.from_bytes(data=buf[:12])
            print(f"Received data from {source}: {buf_data}")
            header = DnsHeader(
                id=1234,
                qr=1,
                opcode=0,
                aa=0,
                tc=0,
                rd=0,
                ra=0,
                z=0,
                rcode=0,
                qdcount=1,
                ancount=1,
                nscount=0,
                arcount=0,
            )
            question = Question(qname="codecrafters.io", qtype=1, qclass=1)
            answer = Answer(
                name="codecrafters.io",
                record_type=1,
                domain_class=1,
                ttl=60,
                rdlength=4,
                rdata="8.8.8.8",
            )
            response = header.to_bytes() + question.to_bytes() + answer.to_bytes()
            print(f"Sending response: {response}")
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
