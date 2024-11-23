import socket  # socket module is used to create a socket object that can communicate with other machines. Socket is basically an endpoint that handles communication between machines and processes. It is a combination of IP address and port number.
from app.utils.header import (
    DnsHeader,
)
from app.utils.question import Question
from app.utils.answer import Answer
from app.logger import log


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    log.info("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            log.debug(f"incoming raw data: {buf}")
            buf_data = DnsHeader.from_bytes(data=buf[:12])
            log.debug(f"parsed header dict: {buf_data}")
            parsed_questions = Question.from_bytes(data=buf)
            log.debug(f"parsed questions: {[q.__dict__ for q in parsed_questions]}")
            flags = DnsHeader.extract_dns_flags(buf_data[1])
            log.debug(f"parsed flags: {flags}")

            answers = [
                Answer(
                    name=question.qname,
                    record_type=1,
                    domain_class=1,
                    ttl=60,
                    rdlength=4,
                    rdata="8.8.8.8",
                )
                for index, question in enumerate(parsed_questions)
            ]
            answer_bytes = b""
            for ans in answers:
                answer_bytes += ans.to_bytes()

            questions_bytes = b""
            for question in parsed_questions:
                questions_bytes += question.to_bytes()

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
                qdcount=len(parsed_questions),
                ancount=len(answers),
                nscount=0,
                arcount=0,
            )
            log.debug(f"response header: {header.__dict__}")
            log.debug(f"response questions:  {[q.__dict__ for q in parsed_questions]}")
            log.debug(f"response answers:  {[a.__dict__ for a in answers]}")
            response = header.to_bytes() + questions_bytes + answer_bytes
            log.debug(f"response bytes: {response}")
            udp_socket.sendto(response, source)
        except Exception as e:
            log.error(f"Error receiving data: {e}", exc_info=True)
            break


if __name__ == "__main__":
    main()
