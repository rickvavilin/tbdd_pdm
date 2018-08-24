__author__ = 'Aleksandr Vavilin'

class LoginFailedException(Exception):
    pass


class UserNotFoundException(LoginFailedException):
    pass


class IncorrectPasswordException(LoginFailedException):
    pass


class DetailNotFoundException(Exception):
    pass


class DetailFileNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class DetailAlreadyExistsException(Exception):
    pass


class FileAlreadyExistsException(Exception):
    pass


class GroupNotFoundException(Exception):
    pass


class GroupAlreadyExistsException(Exception):
    pass


class GroupNotEmptyException(Exception):
    pass


class CycleLinkNotAllowedException(Exception):
    pass


class ActionNotPermitted(Exception):
    pass


class CountMustBeGreaterThanZeroException(Exception):
    pass