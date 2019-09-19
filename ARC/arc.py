def arc(*seq):  # TODO: Прописать ошибки
    """
    This function computing count of variants to connect vertexes on line by non-crossing edges in a half-plane bordered
    by that line.

    :param seq: sequence of degrees (they are integers) of vertexes
    :return: count of variants
    """

    DP = {}

    def prepare(seq):
        i = 0
        while i < len(seq):
            if seq[i] != 0:
                i += 1
            else:
                seq = seq[:i] + seq[i+1:]
        return seq

    seq = prepare(seq)

    Filling = [tuple(seq)]
    New = []
    while Filling:
        for s in Filling:
            s = prepare(s)
            if s not in DP:
                for k in range(1, len(s)):
                    for l in range(s[k]):
                        New += [(*s[1:k], l), (s[0]-1, s[k]-l-1, *s[k+1:])]

            if s == ():
                DP[s] = 1
            elif len(s) == 1:
                DP[s] = 0
            elif sum(s) % 2:
                DP[s] = 0
            else:
                DP[s] = None

        Filling = New
        New = []

    def try_DP(seq):
        if DP[seq] == None:
            DP[seq] = sum([sum([try_DP(prepare((*seq[1:k], l)))*try_DP(prepare((seq[0]-1, seq[k]-l-1, *seq[k+1:]))) for l in range(seq[k])]) for k in range(1, len(seq))])
        return DP[seq]

    return try_DP(seq)


def arc_n_planes(count_of_planes, seq):  # TODO: Прописать ошибки
    """
    This function computing count of variants to connect vertexes on line by non-crossing edges in several half-plane
    bordered by that line.

    :param count_of_planes:
    :param seq:
    :return:
    """
    DP = {}

    def Arc(*seq):
        nonlocal DP

        def prepare(seq):
            i = 0
            while i < len(seq):
                if seq[i] != 0:
                    i += 1
                else:
                    seq = seq[:i] + seq[i + 1:]
            return seq

        seq = prepare(seq)

        Filling = [tuple(seq)]
        New = []
        while Filling:
            for s in Filling:
                s = prepare(s)
                if s not in DP:
                    for k in range(1, len(s)):
                        for l in range(s[k]):
                            New += [(*s[1:k], l), (s[0] - 1, s[k] - l - 1, *s[k + 1:])]

                if s == ():
                    DP[s] = 1
                elif len(s) == 1:
                    DP[s] = 0
                elif sum(s) % 2:
                    DP[s] = 0
                else:
                    '''
                    max_n = -1
                    Sum = 0
                    for n in seq:
                        Sum += n
                        max_n = max(max_n, n)
                    max_n *= 2
                    if max_n > Sum:
                        DP[s] = 0
                    elif max_n == Sum:
                        DP[s] = 1
                    else:
                        DP[s] = None
                    '''
                    DP[s] = None

            Filling = New
            New = []

        def try_DP(seq):
            if DP[seq] == None:
                DP[seq] = sum([sum(
                    [try_DP(prepare((*seq[1:k], l))) * try_DP(prepare((seq[0] - 1, seq[k] - l - 1, *seq[k + 1:]))) for l
                     in range(seq[k])]) for k in range(1, len(seq))])
            return DP[seq]

        return try_DP(seq)

    if count_of_planes == 1:
        return Arc(*seq)

    seq = list(seq)

    def find_n_change():
        nonlocal index, That_half_plane
        index = 0
        while index < len(seq):
            if That_half_plane[index] < seq[index]:
                That_half_plane[index] += 1
                That_half_plane[:index] = [0] * index
                break
            index += 1

    That_half_plane = [0] * len(seq)
    res = arc_n_planes(count_of_planes - 1, seq)
    index = -1
    while That_half_plane != seq:
        find_n_change()
        res += Arc(*That_half_plane) * arc_n_planes(count_of_planes - 1, [seq[i] - That_half_plane[i] for i in range(len(seq))])
    return res
