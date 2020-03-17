PC = 1
MOBILE = 2

def _is_mobile(user_agent: str) -> bool:
    if 'iphone' in user_agent \
        or 'android' in user_agent \
        or 'micromessenger' in user_agent:
        return True
    else:
        return False


def pc_or_mobile(user_agent: str) -> bool:
    user_agent = user_agent.lower()
    if _is_mobile(user_agent):
        return MOBILE
    else:
        return PC