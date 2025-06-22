from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    # Колонки таблицы
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram User ID
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100))

    # Дополнительные поля из вашего старого кода
    balance: Mapped[int] = mapped_column(default=1)
    user_status: Mapped[str] = mapped_column(String(10), default='SR')  # SR, PRO, PM и т.д.
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # Дата регистрации
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    # Связь с действиями пользователя
    actions = relationship("UserAction", back_populates="user")
    # НОВЫЕ ПОЛЯ
    language_code: Mapped[str] = mapped_column(String(2), default='ru')  # ru, en, uz
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=8, nullable=False)

    # Связь для удобного доступа к объекту роли
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Названия роли для кнопок
    name_ru: Mapped[str] = mapped_column(String(100))
    name_en: Mapped[str] = mapped_column(String(100))
    name_uz: Mapped[str] = mapped_column(String(100))

    # Текст системной инструкции
    prompt_ru: Mapped[str] = mapped_column(String(2000))
    prompt_en: Mapped[str] = mapped_column(String(2000))
    prompt_uz: Mapped[str] = mapped_column(String(2000))

    users = relationship("User", back_populates="role")


class UserAction(Base):
    __tablename__ = 'user_actions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    action: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    # Связь с пользователем
    user = relationship("User", back_populates="actions")


class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # ID канала (e.g., -100...)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)  # Ссылка на канал (e.g., https://t.me/...)
    active: Mapped[bool] = mapped_column(Boolean, default=True)  # Активен ли канал для проверки
