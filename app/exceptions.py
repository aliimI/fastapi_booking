from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrentEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует"
)

IncorrectTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный форматик токена"
)

UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров"
)

BookingNotFound = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Бука не найдена"
)

RoomsNotFound = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Комната не найдена"
)

HotelNotFound = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Отель не найден"
)