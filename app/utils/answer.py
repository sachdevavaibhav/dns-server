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
        return (
            self.__encode_qname(self.name)
            + struct.pack(
                ">HHIH", self.type, self.domain_class, self.ttl, self.rdlength
            )
            + self.rdata.encode("ascii")
        )

    def __encode_qname(self, qname):
        parts = qname.split(".")
        result = b""
        for part in parts:
            result += struct.pack("B", len(part)) + part.encode("ascii")
        return result + b"\x00"
