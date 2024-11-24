import struct


class Answer:
    def __init__(
        self,
        name: str,
        record_type: int,
        domain_class: int,
        ttl: int,
        rdlength: int,
        rdata: str,
    ):
        self.name = name
        self.type = record_type
        self.domain_class = domain_class
        self.ttl = ttl
        self.rdlength = rdlength
        self.rdata = rdata

    def to_bytes(self):
        modified_rdata = [int(x) for x in self.rdata.split(".")]
        return (
            self.__encode_qname(self.name)
            + struct.pack(
                ">HHIH", self.type, self.domain_class, self.ttl, self.rdlength
            )
            + struct.pack("!BBBB", *modified_rdata)
        )

    def __encode_qname(self, qname):
        parts = qname.split(".")
        result = b""
        for part in parts:
            result += struct.pack("B", len(part)) + part.encode("ascii")
        return result + b"\x00"

    def __decode_qname(self, data: bytes):
        parts = []
        start = 0
        while True:
            length = data[start]
            if length == 0:
                break
            label = data[start + 1 : start + 1 + length]
            parts.append(label.decode("ascii"))
            start += 1 + length
        return ".".join(parts), start + 1

    @staticmethod
    def from_bytes(data: bytes):
        name, start = Answer.__decode_qname(Answer, data)
        record_type, domain_class, ttl, rdlength = struct.unpack(
            ">HHIH", data[start : start + 10]
        )
        rdata = ".".join(
            [str(x) for x in struct.unpack("!BBBB", data[start + 10 : start + 14])]
        )
        return Answer(name, record_type, domain_class, ttl, rdlength, rdata)
