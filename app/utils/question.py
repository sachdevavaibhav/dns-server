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

    def __parse_qname(self, data, start, parsed_qname={}):
        """
        I will parse the byte data and retur the qname with the next start position
        """
        parts = []
        while True:
            length = data[start]
            if length == 0:
                break
            if (0xC0 & length) == 0xC0:
                pointer = ((length & 0x3F) << 8) | data[start + 1]
                if parsed_qname.get(pointer, None):
                    parts.append(parsed_qname[pointer])
                else:
                    qname, _ = self.__parse_qname(Question, data, pointer, parsed_qname)
                    parts.append(qname)
                start += 1
                break
            label = data[start + 1 : start + 1 + length]
            parts.append(data[start + 1 : start + 1 + length].decode("ascii"))
            parsed_qname[start] = label.decode("ascii")
            start += 1 + length
        return ".".join(parts), start + 1, parsed_qname

    def __parse_questions(self, data, start=12, parsed_qname={}, questions=[]):
        if start >= len(data):
            return questions

        qname, start, new_parsed_qname = self.__parse_qname(
            Question, data=data, start=start, parsed_qname=parsed_qname
        )
        qtype, qclass = struct.unpack(">HH", data[start : start + 4])
        questions.append(Question(qname, qtype, qclass))
        return self.__parse_questions(
            Question, data, start + 4, {**parsed_qname, **new_parsed_qname}, questions
        )

    @staticmethod
    def from_bytes(data):
        # qname, start = Question.__parse_qname(Question, data, 0)
        # qtype, qclass = struct.unpack(">HH", data[start : start + 4])
        # return (qname, qtype, qclass)
        return Question.__parse_questions(
            Question, data=data, parsed_qname={}, questions=[]
        )
