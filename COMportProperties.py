import collections
import ctypes
from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

GENERIC_READ  = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3

INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
ERROR_FILE_NOT_FOUND = 0x0002

class COMMPROP(ctypes.Structure):
    _fields_= (('wPacketLength',       wintypes.WORD),
               ('wPacketVersion',      wintypes.WORD),
               ('dwServiceMask',       wintypes.DWORD),
               ('dwReserved1',         wintypes.DWORD),
               ('dwMaxTxQueue',        wintypes.DWORD),
               ('dwMaxRxQueue',        wintypes.DWORD),
               ('dwMaxBaud',           wintypes.DWORD),
               ('dwProvSubType',       wintypes.DWORD),
               ('dwProvCapabilities',  wintypes.DWORD),
               ('dwSettableParams',    wintypes.DWORD),
               ('dwSettableBaud',      wintypes.DWORD),
               ('wSettableData',       wintypes.WORD),
               ('wSettableStopParity', wintypes.WORD),
               ('dwCurrentTxQueue',    wintypes.DWORD),
               ('dwCurrentRxQueue',    wintypes.DWORD),
               ('dwProvSpec1',         wintypes.DWORD),
               ('dwProvSpec2',         wintypes.DWORD),
               ('wcProvChar',          wintypes.WCHAR * 1))

    class _CONST:
        COMMPROP_INITIALIZED = 0xE73CF52E
        SP_SERIALCOMM = 0x00000001
        BAUD_USER = 0x10000000 # programmable baud rate
        DATABITS_16X = 0x0020 # hardware wide data path

        PROV_SUBTYPE = collections.OrderedDict([
            ('UNSPECIFIED',    0x00000000),
            ('RS232',          0x00000001),
            ('PARALLELPORT',   0x00000002),
            ('RS422',          0x00000003),
            ('RS423',          0x00000004),
            ('RS449',          0x00000005),
            ('MODEM',          0x00000006),
            ('FAX',            0x00000021),
            ('SCANNER',        0x00000022),
            ('NETWORK_BRIDGE', 0x00000100),
            ('LAT',            0x00000101),
            ('TCPIP_TELNET',   0x00000102),
            ('X25',            0x00000103),
        ])

        PROV_CAPABILITIES = collections.OrderedDict([
            ('DTRDSR',        0x0001), # data-terminal-ready / data-set-ready
            ('RTSCTS',        0x0002), # request-to-send / clear-to-send
            ('RLSD',          0x0004), # receive-line-signal-detect
            ('PARITY_CHECK',  0x0008),
            ('XONXOFF',       0x0010), # XON/XOFF flow control
            ('SETXCHAR',      0x0020), # settable XON/XOFF
            ('TOTALTIMEOUTS', 0x0040), # total (elapsed) time-outs
            ('INTTIMEOUTS',   0x0080), # interval time-outs
            ('SPECIALCHARS',  0x0100),
            ('16BITMODE',     0x0200),
        ])

        SETTABLE_PARAMS = collections.OrderedDict([
            ('PARITY',       0x0001),
            ('BAUD',         0x0002),
            ('DATABITS',     0x0004),
            ('STOPBITS',     0x0008),
            ('HANDSHAKING',  0x0010), # flow control
            ('PARITY_CHECK', 0x0020),
            ('RLSD',         0x0040), # receive-line-signal-detect
        ])

        SETTABLE_BAUD = collections.OrderedDict([
            (75,     0x00000001),
            (110,    0x00000002),
            (134.5,  0x00000004),
            (150,    0x00000008),
            (300,    0x00000010),
            (600,    0x00000020),
            (1200,   0x00000040),
            (1800,   0x00000080),
            (2400,   0x00000100),
            (4800,   0x00000200),
            (7200,   0x00000400),
            (9600,   0x00000800),
            (14400,  0x00001000),
            (19200,  0x00002000),
            (38400,  0x00004000),
            (56000,  0x00008000),
            (57600,  0x00040000),
            (115200, 0x00020000),
            (128000, 0x00010000),
        ])

        SETTABLE_DATA = collections.OrderedDict([
            (5,  0x0001), # 5 data bits
            (6,  0x0002), # 6 data bits
            (7,  0x0004), # 7 data bits
            (8,  0x0008), # 8 data bits
            (16, 0x0010), # 16 data bits
        ])

        SETTABLE_STOP = collections.OrderedDict([
            (1,   0x0001), # 1 stop bit
            (1.5, 0x0002), # 1.5 stop bits
            (2,   0x0004), # 2 stop bits
        ])

        SETTABLE_PARITY = collections.OrderedDict([
            ('NONE',  0x0100), # no parity
            ('ODD',   0x0200), # odd parity
            ('EVEN',  0x0400), # even parity
            ('MARK',  0x0800), # mark parity
            ('SPACE', 0x1000), # space parity
        ])

    @property
    def max_baud(self):
        s = self.dwMaxBaud
        m = self._CONST.SETTABLE_BAUD
        if s == self._CONST.BAUD_USER:
            return 0
        else:
            return m[s]

    @property
    def prov_subtype(self):
        s = self.dwProvSubType
        m = self._CONST.PROV_SUBTYPE
        return [x for x, c in m.items() if c & s]

    @property
    def prov_capabilities(self):
        s = self.dwProvCapabilities
        m = self._CONST.PROV_CAPABILITIES
        return [x for x, c in m.items() if c & s]

    @property
    def settable_params(self):
        s = self.dwSettableParams
        m = self._CONST.SETTABLE_PARAMS
        return [x for x, c in m.items() if c & s]

    @property
    def settable_baud(self):
        s = self.dwSettableBaud
        m = self._CONST.SETTABLE_BAUD
        return [x for x, c in m.items() if c & s]

    @property
    def user_settable_baud(self):
        return bool(self.dwSettableBaud & self._CONST.BAUD_USER)

    @property
    def settable_data(self):
        s = self.wSettableData
        m = self._CONST.SETTABLE_DATA
        return [x for x, c in m.items() if c & s]

    @property
    def wide_settable_data(self):
        return bool(self.wSettableData & self._CONST.DATABITS_16X)

    @property
    def settable_stop(self):
        s = self.wSettableStopParity
        m = self._CONST.SETTABLE_STOP
        return [x for x, c in m.items() if c & s]

    @property
    def settable_parity(self):
        s = self.wSettableStopParity
        m = self._CONST.SETTABLE_PARITY
        return [x for x, c in m.items() if c & s]


LPCOMMPROP = ctypes.POINTER(COMMPROP)

class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = (('nLength',              wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle',       wintypes.BOOL))

LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)

kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.CreateFileW.argtypes = (
    wintypes.LPCWSTR,      # _In_     lpFileName
    wintypes.DWORD,        # _In_     dwDesiredAccess
    wintypes.DWORD,        # _In_     dwShareMode
    LPSECURITY_ATTRIBUTES, # _In_opt_ lpSecurityAttributes
    wintypes.DWORD,        # _In_     dwCreationDisposition
    wintypes.DWORD,        # _In_     dwFlagsAndAttributes
    wintypes.HANDLE)       # _In_opt_ hTemplateFile

kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)

kernel32.GetCommProperties.argtypes = (
    wintypes.HANDLE, # _In_  hFile
    LPCOMMPROP)      # _Out_ lpCommProp

def get_comm_properties(handle_or_port):
    if isinstance(handle_or_port, str):
        handle = kernel32.CreateFileW(
                        handle_or_port,
                        GENERIC_READ | GENERIC_WRITE,
                        0,    # exclusive access
                        None, # default security
                        OPEN_EXISTING,
                        0,
                        None)
        if handle == INVALID_HANDLE_VALUE:
            raise ctypes.WinError(ctypes.get_last_error())
        close_handle = True
    else:
        handle = handle_or_port
        close_handle = False
    try:
        prop = COMMPROP()
        if not kernel32.GetCommProperties(handle, ctypes.byref(prop)):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        if close_handle:
            kernel32.CloseHandle(handle)
    return prop

if __name__ == '__main__':
    for i in range(1, 20):
        port = r'\\.\COM%d' % i
        try:
            prop = get_comm_properties(port)
        except WindowsError as e:
            if e.winerror == ERROR_FILE_NOT_FOUND:
                continue
        print('%s properties' % port)
        x = prop.dwMaxTxQueue if prop.dwMaxTxQueue else 'no limit'
        print('\tMax output buffer size: %s' % x)
        x = prop.dwMaxRxQueue if prop.dwMaxRxQueue else 'no limit'
        print('\tMax input buffer size: %s' % x)
        x = prop.dwCurrentTxQueue if prop.dwCurrentTxQueue else 'unavailable'
        print('\tCurrent output buffer size: %s' % x)
        x = prop.dwCurrentRxQueue if prop.dwCurrentRxQueue else 'unavailable'
        print('\tCurrent input buffer size: %s' % x)
        x = prop.max_baud if prop.max_baud else 'user programmable'
        print('\tMax baud rate: %s' % x)
        print('\tProvider subtypes:\n\t\t%s' %
                    '\n\t\t'.join(prop.prov_subtype))
        print('\tProvider capabilities:\n\t\t%s' %
                    '\n\t\t'.join(prop.prov_capabilities))
        print('\tSettable parameters:\n\t\t%s' %
                    '\n\t\t'.join(prop.settable_params))
        print('\tSettable baud rates:\n\t\t%s' %
                    '\n\t\t'.join([str(x) for x in prop.settable_baud]))
        print('\tSettable user baud rates: %s' %
                    prop.user_settable_baud)
        print('\tSettable data bits:\n\t\t%s' %
                    '\n\t\t'.join([str(x) for x in prop.settable_data]))
        print('\tSettable wide data bits: %s' %
                    prop.wide_settable_data)
        print('\tSettable stop bits:\n\t\t%s' %
                    '\n\t\t'.join([str(x) for x in prop.settable_stop]))
        print('\tSettable parity:\n\t\t%s' %
                    '\n\t\t'.join(prop.settable_parity))