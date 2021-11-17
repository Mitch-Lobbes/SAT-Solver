def negate_literal(literal: str) -> str:
    return f"-{literal}" if not "-" in literal else literal[1:]