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
            print(buf[12:])
            buf_data = DnsHeader.from_bytes(data=buf[:12])
            buf_question = Question.from_bytes(data=buf[12:])
            print(buf_question)
            # print(f"Received data from {source}: {buf_data}")
            flags = DnsHeader.extract_dns_flags(buf_data[1])
            print(flags)
            header = DnsHeader(
                id=buf_data[0],
                qr=1,
                opcode=flags["opcode"],
                aa=0,
                tc=0,
                rd=flags["rd"],
                ra=0,
                z=0,
                rcode=0 if flags["opcode"] == 0 else 4,
                qdcount=1,
                ancount=1,
                nscount=0,
                arcount=0,
            )
            question = Question(
                qname=buf_question[0], qtype=buf_question[1], qclass=buf_question[2]
            )
            answer = Answer(
                name=buf_question[0],
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
