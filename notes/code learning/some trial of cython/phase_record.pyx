

# phase_record.pyx
cdef public class PhaseRecord(object)[type PhaseRecordType, object PhaseRecordObject]:
    cdef public double temperature

    def __init__(self, double temperature):
        self.temperature = temperature

