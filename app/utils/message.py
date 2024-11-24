import socket
from app.utils.header import DnsHeader
from app.utils.question import Question
from app.utils.answer import Answer
from app.logger import log
from typing import List


class DnsMessage:
    def __init__(self, data: bytes):
        self.data: bytes = data
        self.header: "DnsHeader" = DnsHeader.from_bytes(data[:12])
        self.questions: List["Question"] = Question.from_bytes(data)
        # self.flags: dict = DnsHeader.extract_dns_flags(self.data[1])
        self.answers: List["Answer"] = []

    def add_answer(self):
        self.answers = [
            Answer(
                name=question.qname,
                record_type=1,
                domain_class=1,
                ttl=60,
                rdlength=4,
                rdata="8.8.8.8",
            )
            for index, question in enumerate(self.questions)
        ]

    def respond(self):
        answer_bytes = b""
        for ans in self.answers:
            answer_bytes += ans.to_bytes()

        questions_bytes = b""
        for question in self.questions:
            questions_bytes += question.to_bytes()
        log.debug(f"Flag: {self.header.__dict__}")
        # header = DnsHeader(
        #     id=self.header.id,
        #     qr=1,
        #     opcode=self.flags["opcode"],
        #     aa=0,
        #     tc=0,
        #     rd=self.flags["ra"],
        #     ra=0,
        #     z=0,
        #     rcode=0 if self.flags["opcode"] == 0 else 4,
        #     qdcount=len(self.questions),
        #     ancount=len(self.answers),
        #     nscount=0,
        #     arcount=0,
        # )
        self.header.qr = 1
        self.header.rcode = 0 if self.header.opcode == 0 else 4
        self.header.qdcount = len(self.questions)
        self.header.ancount = len(self.answers)

        return self.header.to_bytes() + questions_bytes + answer_bytes

    def forward(self, resolver: str):
        resolver_parts = resolver.split(":")
        resolver_ip = resolver_parts[0]
        resolver_port = int(resolver_parts[1])

        for question in self.questions:
            message_header = DnsHeader(
                id=self.header.id,
                qr=self.header.qr,
                opcode=0,
                aa=self.header.aa,
                tc=self.header.tc,
                rd=self.header.rd,
                ra=self.header.ra,
                z=self.header.z,
                rcode=self.header.rcode,
                qdcount=1,
                ancount=self.header.ancount,
                nscount=self.header.nscount,
                arcount=self.header.arcount,
            )
            message = message_header.to_bytes() + question.to_bytes()
            message_length = len(message)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                udp_socket.sendto(message, (resolver_ip, resolver_port))
                response, _ = udp_socket.recvfrom(512)
                log.debug(response)
                answer = Answer.from_bytes(response[message_length:])
                self.answers.append(answer)
