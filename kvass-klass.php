<?php
/**
 * Тестовая задачка про аппарат с Квасс-Классом
 * 
 * https://contest.yandex.ru/algorithm2018/contest/8254/problems/?nc=00PX9ohW
 * 
 * Использование: php kvass-klass.php [filename] [debugflag]
 *     filename = по-умолчанию input.txt
 *     debugflag = true или что угодно (=>false)
 */


const MILLION = 10**6;


function readInputFile($filename)
{
    if (!file_exists($filename)) return false;
    $file = file_get_contents($filename);
    $lines = explode("\n", $file);
    return $lines;
}


function showBalance($state, $fromWhere = 0)
{
    global $debug;
    if (!$debug) {
        return;
    }

    print_r([$fromWhere => $state]);
    print("\n");
}


function checkRequirements($state)
{
    return $state['priceBottle'] >= 1;
}


function runCalc($fileName): array
{
    $state = array();

    // Сколько бутылок сможет купить 
    $state['bottles'] = 0;

    // Неправильный файл
    if (!($fileContent = readInputFile($fileName))) {
        return $state;
    }

    // Берем две строки
    [$firstLine, $secondLine] = $fileContent;

    // Строим начальное состояние
    [$state['userMillions'], $state['userCoins']] = explode(' ', $firstLine);
    [$state['priceBottle'], $state['deviceCoins']] = explode(' ', $secondLine);

    // Приводим к целому
    foreach(['userMillions', 'userCoins', 'priceBottle', 'deviceCoins'] as $index => $elem) {
        $state[$elem] = intval($state[$elem]);
    }

    // Количество миллионов в аппарате не важно, будем считать что их нет
    $state['deviceMillions'] = 0;

    // Что-то не так
    if (!checkRequirements($state)) {
        return $state;
    }

    // Покажем начальное состояние
    showBalance($state, 'подошли к аппарату');

    do {
        $goNextStep = false;

        // Если у пользователя точно сколько нужно
        $needCoins = $state['priceBottle'] % MILLION;
        $needMillions = intval($state['priceBottle'] / MILLION);
        if ($state['userCoins'] >= $needCoins && $state['userMillions'] >= $needMillions) {
            $state['userCoins'] -= $needCoins;
            $state['deviceCoins'] += $needCoins;
            $state['userMillions'] -= $needMillions;
            $state['deviceMillions'] += $needMillions;
            $state['bottles'] ++;
            showBalance($state, 'есть точно сколько нужно');
            $goNextStep = true;
            continue;
        }

        // Если не хватит - пытаемся потратить миллионы (но это если они остались)
        if ($state['userMillions'] > 0) {
            // Сколько нужно в аппарате для сделки?
            $needToRefundCoins = MILLION - ($state['priceBottle'] % MILLION);
            $needToRefundMillions = 1 + intval($state['priceBottle'] / MILLION);

            // Не хватило
            if ($state['deviceCoins'] < $needToRefundCoins) {
                continue;
            }

            // Пересчитаем балансы
            $state['userCoins'] += $needToRefundCoins;
            $state['deviceCoins'] -= $needToRefundCoins;
            $state['deviceMillions'] += $needToRefundMillions;
            $state['userMillions'] -= $needToRefundMillions; 
            // Купили еще одну бутылку!
            $state['bottles'] ++;

            showBalance($state, 'с миллиона сдадите?');
            $goNextStep = true;
            continue;
        }
    }
    while ($goNextStep);

    return $state;
}


function main()
{
    // Определяем параметры запуска
    $inputFile = $params[1] ?? __DIR__ . '/input.txt';
    $debug = ($params[2] ?? 'false') == 'true';
    
    // Запускам
    $result = runCalc($inputFile);
    print($result['bottles'] . "\n");
}


main();
