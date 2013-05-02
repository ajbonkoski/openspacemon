
def format_number(separator, n):
    """format number with a 'separator'"""
    n_s = str(n)
    if len(n_s) <= 3:
        return n_s
    else:
        upper = n_s[:-3]
        lower = n_s[-3:]
        return format_number(separator, upper) + separator + lower

