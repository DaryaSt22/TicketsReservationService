import db



def app():
    db.init_db()
    print("Вас приветствует сервис резервирования билетов!")
    while True:
        print("Выберете нужную команду: ")
        print("0. Выход")
        print("1. Показать список мероприятий")
        print("2. Показать список мест")
        print("3. Показать список билетов")
        print("4. Показать детальную информацию по id мероприятия")
        print("5. ")# events and tickets
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
        else:
            print("Вы ввели несуществующую команду. Попробуйте еще раз!")


app()