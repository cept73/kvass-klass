# coding=utf-8
"""
    Тестовая задачка про аппарат с Квасс-Классом

    https://contest.yandex.ru/algorithm2018/contest/8254/problems/?nc=00PX9ohW

    Использование: python kvass-klass.py [filename] [debugflag]
        filename = по-умолчанию input.txt
        debugflag = true или что угодно (=>false)
"""
import os
import sys


# Константа Миллион = 10^6
MILLION = 10**6


def loadStateFromFile(filename):
    # Начальное состояние
    state = {}

    # Сколько бутылок сможет купить
    state['bottles'] = 0

    # Не существует?
    if not os.path.exists(filename):
        return False

    # Открываем файл
    inputFile = open(filename)

    # Бежим считая строки
    lineNo = 1

    # Пробегаем построчно
    for line in inputFile:
        # Дальше второй строки идти не нужно
        if lineNo > 2:
            break

        # Убираем спец.символы
        line = line.strip("\n")

        try:
            # Считываем колонки
            cols = line.split(' ')
        except Exception:
            # Плохой файл
            return False

        # С первой и второй строки берем разные вещи
        if lineNo == 1:
            state['userMillions'] = int(cols[0])
            state['userCoins'] = int(cols[1])
        elif lineNo == 2:
            state['priceBottle'] = int(cols[0])
            state['deviceCoins'] = int(cols[1])

        # Следующая строка
        lineNo += 1

    # Для начала пусть в аппарате будет 0 миллионов (не указано в задаче)
    state['deviceMillions'] = 0

    return state


def showBalance(state, fromWhere=0):
    # В обычном режиме ничего не пишет
    if not debugFlag:
        return

    # Работает только при включенном debug
    print({fromWhere: state})


def checkRequirements(state):
    # Требований не так много
    # При цене бутылки 0 - зависнет
    return state['priceBottle'] >= 1


def main(fileName):
    # Грузим файл с входными данными
    state = loadStateFromFile(fileName)

    # Какой то неправильный файл
    if not state:
        return False

    # Что-то не так
    if not checkRequirements(state):
        return state

    # Покажем начальное состояние
    showBalance(state, 'подошли к аппарату')

    # Пока не выполнятся условия задачи..
    goNextStep = True
    while goNextStep:
        goNextStep = False

        # Если у пользователя точно сколько нужно
        needCoins = state['priceBottle'] % MILLION
        needMillions = state['priceBottle'] / MILLION
        if state['userCoins'] >= needCoins:
            if state['userMillions'] >= needMillions:
                state['userCoins'] -= needCoins
                state['deviceCoins'] += needCoins
                state['userMillions'] -= needMillions
                state['deviceMillions'] += needMillions
                state['bottles'] += 1
                showBalance(state, 'есть точно сколько нужно')
                goNextStep = True
                continue

        # Монет хватит? Сдачи не надо
        if state['userCoins'] >= state['priceBottle']:
            # Пересчитаем
            state['userCoins'] -= state['priceBottle']
            state['deviceCoins'] += state['priceBottle']
            state['bottles'] += 1
            showBalance(state, 'хватает мелочи')
            goNextStep = True
            continue

        # Если не хватит - пытаемся потратить миллионы (если они остались)
        if state['userMillions'] > 0:
            needToRefundCoins = MILLION - (state['priceBottle'] % MILLION)
            needToRefundMillions = 1 + int(state['priceBottle'] / MILLION)

            # Не хватит сдачи с миллиона
            if state['deviceCoins'] < needToRefundCoins:
                continue

            # Произведем покупку, пересчитаем баланс
            state['userCoins'] += needToRefundCoins
            state['deviceCoins'] -= needToRefundCoins
            state['deviceMillions'] += needToRefundMillions
            state['userMillions'] -= needToRefundMillions
            # Купили еще одну бутылку!
            state['bottles'] += 1

            showBalance(state, 'с миллиона сдадите?')
            goNextStep = True
            continue

    return state


if __name__ == '__main__':
    # Определяем параметры из коммандной строки либо default
    args = sys.argv
    argsLen = len(args)

    # Входные параметры по-умолчанию
    inputFile = "input.txt"
    debugFlag = False

    # Параметры указанные в коммандной строке
    if argsLen > 1:
        inputFile = args[1]
    if argsLen > 2:
        debugFlag = args[2] == 'true'

    # Начальное состояние находится в указанном файле
    result = main(inputFile)

    # Выводим результат
    if result:
        # Сколько бутылок у программиста
        print(result['bottles'])
    else:
        # Не получилось
        print("Ошибка")
