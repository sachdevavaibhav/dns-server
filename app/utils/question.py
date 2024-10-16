import struct


class Question:
    def __init__(self, qname, qtype, qclass):
        self.qname: str = qname
        self.qtype: int = qtype
        self.qclass: int = qclass

    def to_bytes(self):
        return self.__encode_qname(self.qname) + struct.pack(
            ">HH", self.qtype, self.qclass
        )

    def __encode_qname(self, qname):
        parts = qname.split(".")
        result = b""
        for part in parts:
            result += struct.pack("B", len(part)) + part.encode("ascii")
        return result + b"\x00"
