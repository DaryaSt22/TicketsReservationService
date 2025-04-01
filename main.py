import db
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship

DATABASE_URL = "postgresql://postgres:secret@localhost/test"

Base = DeclarativeBase()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine, expire_on_commit=False)

engine = create_engine(DATABASE_URL)
class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(100), unique= True, index = True)

    seats = relationship("EventsSeats", back_populates= "event")
    tickets = relationship("EventsTickets", back_populates="event")

class Seat(Base):
    __tablename__ = "Seats"

    id = Column(Integer, primary_key = True, index = True)
    seat_name = Column(String(100), unique= True, index = True)

    events = relationship("EventsSeats", back_populates= "seat")

class Ticket(Base):
    __tablename__ = "Ticket"

    id = Column(Integer, primary_key=True, index=True)
    ticket_name = Column(String(100), unique=True, index=True)

    events = relationship("EventsTickets", back_populates="ticket")

class PRIMARYKey:
    pass

class EventsSeats(Base):
    __tablename__ = "Events_seats"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, PRIMARYKey("events.id", ondelete="CASCADE"))
    seat_id = Column(Integer, PRIMARYKey("seats.id", ondelete="CASCADE"))

    event = relationship("Event", back_populates="seats")
    seat = relationship("Seat", back_populates="events")

class EventsTickets(Base):
    __tablename__ = "Events_tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, PRIMARYKey("events.id", ondelete="CASCADE"))
    ticket_id = Column(Integer, PRIMARYKey("tickets.id", ondelete="CASCADE"))

    event = relationship("Event", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="events")

    Base.metadata.create_all(engine)

def init_db():
    print("База данных инициализирована!")

def get_all_events():
    with SessionLocal() as session:
        return session.query(Event).all()

def print_menu():
    print("Выберете нужную команду: ")
    print("0. Выход")
    print("1. Показать список мероприятий")
    print("2. Показать список мест")
    print("3. Показать список билетов")
    print("4. Показать детальную информацию по id мероприятия")
    print("5. Добавить мероприятие")
    print("6. Поиск мероприятия по названию")
    print("7. Удаление мероприятия")
    print("8. Редактирование мероприятия")
    print("9. Добавить место(seat)")
    print("10. Удалить место(seat)")
    print("11. Редактирование места(seat)")


def app():
    db.init_db()
    print("Вас приветствует сервис резервирования билетов!")
    while True:
        print_menu()
        cmd = int(input("Введите номер команды: "))

        if cmd == 0:
            print("До скорой встречи")
            break
        elif cmd == 1:
            print("=" * 20)
            print("\nСписок мероприятий: ")
            events = db.get_all_events()
            for event in events:
                print(f"ID: {event[0]} - Title: {event[1]}.")
            print("=" * 20)

        elif cmd == 2:
            print("=" * 20)
            print("\nСписок мест: ")
            seats = db.get_all_seats()
            for seat in seats:
                print(f"ID: {seat[0]} - Seat: {seat[1]}.")
            print("=" * 20)

        elif cmd == 3:
            print("=" * 20)
            print("\nСписок билетов: ")
            tickets = db.get_all_tickets()
            for ticket in tickets:
                print(f"ID: {ticket[0]} - Ticket: {ticket[1]}.")
            print("=" * 20)

        elif cmd == 4:
            print("=" * 20)
            print("\nИнформация по мероприятию: ")
            event_id = int(input("Введите id мероприятия: "))
            event_details = db.get_event_info_by_id(event_id)
            if event_details is None:
                print("Нет такого мероприятия!")
            else:
                event_info = event_details["event_info"]
                print(f' ID: {event_info[0]} - Название: {event_info[1]}')

                seats = event_details["seats"]
                print("Места: ")
                for seat in seats:
                    print(seat[0], end=" | ")

                tickets = event_details["tickets"]
                print("\nБилеты: ")
                for ticket in tickets:
                    print(ticket[0], end=" | ")
                print()
            print("=" * 20)

        elif cmd == 5:
            print("=" * 20)
            print("Добавление нового мероприятия: ")
            title = input("Введите название мероприятия: ")
            try:
                db.create_event(title)
                print("Мероприятие успешно создано!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)

        elif cmd == 6:
            print("=" * 20)
            query = input("Введите название или часть название мероприятия: ")

            events = db.search_event(query)
            for event in events:
                print(f"ID: {event[0]} - Title: {event[1]}.")
            print("=" * 20)

        elif cmd == 7:
            print("=" * 20)
            query_delete = input("Введите название мероприятия, которое нужно удалить: ")
            try:
                db.delete_event(query_delete)
                print("Мероприятие успешно удалено!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 8:
            print("=" * 20)
            event_name = input("Введите название мероприятия, которое нужно отредактировать: ")
            new_event_name = input("Введите новое название мероприятия: ")
            try:
                db.edit_event(event_name, new_event_name)
                print("Мероприятие успешно отредактировано!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 9:
            print("=" * 20)
            print("Добавление нового места: ")
            seat_name = input("Введите номер места: ")
            try:
                db.create_seat(int(seat_name))
                print("Номер места успешно добавлен!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)

        elif cmd == 10:
            print("=" * 20)
            query_delete = input("Введите номер места, которое нужно удалить: ")
            try:
                db.delete_seat(int(query_delete))
                print("Номер места успешно удален!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 11:
            print("=" * 20)
            seat_name = input("Введите номер места, которое нужно отредактировать: ")
            new_seat_name = input("Введите новый номер места(seat): ")
            try:
                db.edit_seat(seat_name, new_seat_name)
                print("Номер места(seat) успешно отредактирован!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")


        else:
            print("Вы ввели несуществующую команду. Попробуйте еще раз!")

app()