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

    def __parse_qname(self, data, start):
        parts = []
        while True:
            length = data[start]
            if length == 0:
                break
            parts.append(data[start + 1 : start + 1 + length].decode("ascii"))
            start += 1 + length
        return ".".join(parts), start + 1

    @staticmethod
    def from_bytes(data):
        qname, start = Question.__parse_qname(Question, data, 0)
        qtype, qclass = struct.unpack(">HH", data[start : start + 4])
        return (qname, qtype, qclass)
