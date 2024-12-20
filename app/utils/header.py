import struct
from app.logger import log


class DnsHeader:
    def __init__(
        self,
        id: int,
        qr: int,
        opcode: int,
        aa: int,
        tc: int,
        rd: int,
        ra: int,
        z: int,
        rcode: int,
        qdcount: int,
        ancount: int,
        nscount: int,
        arcount: int,
    ):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.rcode = rcode
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

    def to_bytes(self):
        flags = (
            self.qr << 15
            | self.opcode << 11
            | self.aa << 10
            | self.tc << 9
            | self.rd << 8
            | self.ra << 7
            | self.z << 4
            | self.rcode
        )
        return struct.pack(
            "!6H",
            self.id,
            flags,
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount,
        )

    @staticmethod
    def from_bytes(data):
        id, flags_int, qdcount, ancount, nscount, arcount = struct.unpack("!6H", data)
        flags = DnsHeader.extract_dns_flags(flags_int)
        return DnsHeader(
            id=id,
            qr=flags["qr"],
            opcode=flags["opcode"],
            aa=flags["aa"],
            tc=flags["tc"],
            rd=flags["rd"],
            ra=flags["ra"],
            z=flags["z"],
            rcode=flags["rcode"],
            qdcount=qdcount,
            ancount=ancount,
            nscount=nscount,
            arcount=arcount,
        )

    @staticmethod
    def extract_dns_flags(flag):
        log.debug(f"Received Flag: {flag}")
        qr = flag >> 15 & 0x1
        opcode = flag >> 11 & 0xF
        aa = flag >> 10 & 0x1
        tc = flag >> 9 & 0x1
        rd = flag >> 8 & 0x1
        ra = flag >> 7 & 0x1
        z = flag >> 4 & 0x7
        rcode = flag & 0xF

        return {
            "qr": qr,
            "opcode": opcode,
            "aa": aa,
            "tc": tc,
            "rd": rd,
            "ra": ra,
            "z": z,
            "rcode": rcode,
        }

    def __str__(self):
        return f"id={self.id}, qr={self.qr}, opcode={self.opcode}, aa={self.aa}, tc={self.tc}, rd={self.rd}, ra={self.ra}, z={self.z}, rcode={self.rcode}, qdcount={self.qdcount}, ancount={self.ancount}, nscount={self.nscount}, arcount={self.arcount}"


# | RFC Name | Descriptive Name     | Length             | Description                                                                                                                                                                         |
# | -------- | -------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
# | ID       | Packet Identifier    | 16 bits            | A random identifier is assigned to query packets. Response packets must reply with the same id. This is needed to differentiate responses due to the stateless nature of UDP.       |
# | QR       | Query Response       | 1 bit              | 0 for queries, 1 for responses.                                                                                                                                                     |
# | OPCODE   | Operation Code       | 4 bits             | Typically always 0, see RFC1035 for details.                                                                                                                                        |
# | AA       | Authoritative Answer | 1 bit              | Set to 1 if the responding server is authoritative - that is, it "owns" - the domain queried.                                                                                       |
# | TC       | Truncated Message    | 1 bit              | Set to 1 if the message length exceeds 512 bytes. Traditionally a hint that the query can be reissued using TCP, for which the length limitation doesn't apply.                     |
# | RD       | Recursion Desired    | 1 bit              | Set by the sender of the request if the server should attempt to resolve the query recursively if it does not have an answer readily available.                                     |
# | RA       | Recursion Available  | 1 bit              | Set by the server to indicate whether or not recursive queries are allowed.                                                                                                         |
# | Z        | Reserved             | 3 bits             | Originally reserved for later use, but now used for DNSSEC queries.                                                                                                                 |
# | RCODE    | Response Code        | 4 bits             | Set by the server to indicate the status of the response, i.e. whether or not it was successful or failed, and in the latter case providing details about the cause of the failure. |
# | QDCOUNT  | Question Count       | 16 bits            | The number of entries in the Question Section                                                                                                                                       |
# | ANCOUNT  | Answer Count         | 16 bits            | The number of entries in the Answer Section                                                                                                                                         |
# | NSCOUNT  | Authority Count      | 16 bits            | The number of entries in the Authority Section                                                                                                                                      |
# | ARCOUNT  | Additional Count     | 16 bits            | The number of entries in the Additional Section
