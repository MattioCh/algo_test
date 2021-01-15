import enum

class s(enum.Enum): #States
    Error           = 0
    INITIATE        = 1
    FIRST_1000_DAYS = 2
    PROCESS_DATA    = 3
    MAKE_ORDER      = 4
    EXCEED_LEVERAGE = 5
    PRINT_LOG       = 6
    EXIT_FSM        = 7

    pass


'''             Trigger             Prev State          Next State'''

transitions_ = [["initiate",        s.INITIATE ,        s.FIRST_1000_DAYS],
                ["proceed",         s.FIRST_1000_DAYS,  s.PROCESS_DATA],
                ["proceed",         s.PROCESS_DATA,     s.MAKE_ORDER],
                ["proceed",         s.MAKE_ORDER,       s.PRINT_LOG],
                ["exceed_leverage", s.MAKE_ORDER,       s.EXCEED_LEVERAGE],
                ["proceed",         s.EXCEED_LEVERAGE,  s.PRINT_LOG],
                ["print_log",       s.PRINT_LOG,        s.EXIT_FSM],
                ["exit",            s.EXIT_FSM,         s.EXIT_FSM]
                                                                            ]