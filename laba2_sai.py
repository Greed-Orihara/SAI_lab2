# тема: диагностика аппаратного обеспечения ПК
# лабораторная №2: обратная цепочка рассуждений

facts = {}
rules = []


def load_rules():
    global rules
    rules = []
    f = open("rules.txt", "r", encoding="utf-8")
    for line in f:
        line = line.strip()
        if line != "":
            rules.append(line)
    f.close()


def show_facts():
    print("\n Собранные факты \n")
    if len(facts) == 0:
        print("Данных пока нет")
    else:
        for key in facts:
            print(key + " = " + facts[key])
    print("______________________________")


def add_fact(name, value):
    facts[name] = value


def has_fact(name, value):
    if name in facts:
        if facts[name] == value:
            return True
    return False


def parse_rule(rule):
    if " ТО " not in rule:
        return None, None
    parts = rule.split(" ТО ")
    uslovie = parts[0]
    vyvod = parts[1]
    if uslovie.startswith("ЕСЛИ "):
        uslovie = uslovie[5:]
    conditions = uslovie.split(" И ")
    return conditions, vyvod


def check_condition(cond):
    if "=" not in cond:
        return False
    pair = cond.split("=")
    name = pair[0].strip()
    value = pair[1].strip()

    if has_fact(name, value):
        print("  " + name + "=" + value + " — есть в фактах")
        return True

    print("  " + name + "=" + value + " — нет в фактах")
    answer = input("  Это верно? (да/нет): ").strip()
    if answer.lower() == "да":
        add_fact(name, value)
        return True
    return False


def prove(goal_name, goal_value):
    print("\n--- Доказательство цели: " + goal_name + "=" + goal_value + " ---")

    if has_fact(goal_name, goal_value):
        print("Цель уже есть в фактах. Доказано.")
        return True

    for rule in rules:
        conditions, vyvod = parse_rule(rule)
        if conditions is None:
            continue

        # Проверяем, выводит ли это правило нашу цель
        if "=" in vyvod:
            pair = vyvod.split("=")
            v_name = pair[0].strip()
            v_value = pair[1].strip()
            
            if v_name == goal_name and v_value == goal_value:
                print("Найдено правило: " + rule)
                print("Проверяю условия:")
                
                all_ok = True
                for cond in conditions:
                    if not check_condition(cond):
                        all_ok = False
                        break
                
                if all_ok:
                    print("Все условия выполнены.")
                    add_fact(goal_name, goal_value)
                    return True
                else:
                    print("Не все условия выполнены.")

    print("Нет правила, которое выводит эту цель.")
    return False


def main():
    load_rules()

    print(" Система диагностики ПК (обратная цепочка) ")
    print("ВНИМАНИЕ: значения пишите с подчеркиваниями (например: Неисправен_БП)")

    while True:
        # 1. Вводим факты
        print("\nВведите начальные факты.")
        while True:
            name = input("Имя объекта (или 'нет' для продолжения): ").strip()
            if name.lower() == "нет":
                break
            value = input("Значение: ").strip()
            add_fact(name, value)

        show_facts()

        # 2. Вводим цель (руками)
        print("\nВведите целевую ситуацию.")
       
        goal_name = input("Имя объекта (например, Причина): ").strip()
        goal_value = input("Значение (например, Неисправна_видеокарта): ").strip()

        # 3. Доказываем
        result = prove(goal_name, goal_value)

        # 4. Результат
        print("\n=== РЕЗУЛЬТАТ ===")
        if result:
            print("ЦЕЛЬ ДОКАЗАНА: " + goal_name + "=" + goal_value)
        else:
            print("ЦЕЛЬ ОПРОВЕРГНУТА: " + goal_name + "=" + goal_value)
        print("==================")

        show_facts()

        # 5. Меню
        print("\n1. Очистить базу и начать заново")
        print("2. Выйти")
        choice = input("Выбор: ").strip()

        if choice == "1":
            facts.clear()
            print("База очищена.")
        elif choice == "2":
            print("Работа завершена.")
            break


main()