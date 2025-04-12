/**
 * Table Formatter - скрипт для форматирования значений в таблице
 * Автоматически форматирует даты и числа после рендеринга таблицы
 */

(function() {
  // Состояние - найдены ли таблицы
  let tablesFound = false;
  
  /**
   * Главная функция форматирования значений в таблице
   */
  function formatTableValues() {
    console.log('Поиск таблиц для форматирования...');
    
    // Ищем таблицу с указанными классами
    const tables = document.querySelectorAll('table.min-w-full');
    
    if (!tables.length) {
      // Расширенный поиск - ищем любые таблицы на странице
      const allTables = document.querySelectorAll('table');
      
      if (allTables.length) {
        console.log(`Найдено ${allTables.length} таблиц, но без класса min-w-full.`);
        allTables.forEach((table, index) => {
          console.log(`Таблица #${index + 1}, классы: ${table.className}`);
          // Пробуем обработать их тоже
          processTable(table);
        });
        tablesFound = true;
        return;
      } else {
        console.log('Таблицы на странице не найдены');
        return;
      }
    }
    
    console.log(`Найдено ${tables.length} таблиц для форматирования`);
    tablesFound = true;
    
    // Обрабатываем каждую таблицу
    tables.forEach(table => {
      processTable(table);
    });
  }
  
  /**
   * Обрабатывает отдельную таблицу
   * @param {HTMLElement} table - Элемент таблицы для обработки
   */
  function processTable(table) {
    try {
      console.log('Обработка таблицы:', table);
      
      // Получаем заголовки
      const headerRow = table.querySelector('thead tr');
      if (!headerRow) {
        console.log('Строка заголовков не найдена');
        return;
      }
      
      const headers = Array.from(headerRow.querySelectorAll('th'));
      const columnTypes = {};
      
      console.log(`Найдено ${headers.length} заголовков`);
      
      // Определяем типы столбцов по названиям заголовков
      headers.forEach((header, index) => {
        const headerText = header.textContent.toLowerCase().trim();
        console.log(`Заголовок ${index}: "${headerText}"`);
        
        // Определяем тип данных по тексту заголовка
        if (headerText.includes('дата') || headerText.includes('date') || 
            headerText.includes('время') || headerText.includes('time')) {
          columnTypes[index] = 'date';
        } 
        else if (headerText.includes('сумма') || headerText.includes('amount') || 
                 headerText.includes('число') || headerText.includes('number') ||
                 headerText.includes('цена') || headerText.includes('price') ||
                 headerText.includes('кол-во') || headerText.includes('quantity')) {
          columnTypes[index] = 'number';
        }
        
        // Также проверяем атрибуты, если они есть
        if (header.hasAttribute('data-type')) {
          columnTypes[index] = header.getAttribute('data-type');
        }
      });
      
      console.log('Определенные типы столбцов:', columnTypes);
      
      // Применяем форматирование к ячейкам таблицы
      const rows = table.querySelectorAll('tbody tr');
      console.log(`Найдено ${rows.length} строк для форматирования`);
      
      let processedCells = 0;
      
      // Обрабатываем каждую строку
      rows.forEach((row, rowIndex) => {
        if (rowIndex > 50) {
          // Ограничиваем количество строк для первоначальной обработки
          return;
        }
        
        const cells = row.querySelectorAll('td');
        
        // Обрабатываем каждую ячейку в строке
        cells.forEach((cell, cellIndex) => {
          // Получаем div внутри ячейки для доступа к данным, как показано в HTML-структуре
          const divWithData = cell.querySelector('div');
          // Внутри div может быть span с данными
          const spanWithData = divWithData ? divWithData.querySelector('span') : null;
          
          // Выбираем элемент для форматирования (span, div или сама ячейка)
          const elementToFormat = spanWithData || divWithData || cell;
          
          if (!elementToFormat) return;
          
          // Проверяем, есть ли у ячейки атрибут data-type
          let cellType = cell.getAttribute('data-type');
          
          // Если нет атрибута, используем тип из заголовка
          if (!cellType && columnTypes[cellIndex]) {
            cellType = columnTypes[cellIndex];
          }
          
          // Если нет информации о типе, пытаемся угадать
          if (!cellType) {
            const text = elementToFormat.textContent.trim();
            
            // Проверяем, похоже ли значение на дату ISO
            if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(text) || 
                /^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/.test(text) ||
                /^\d{4}-\d{2}-\d{2}$/.test(text)) {
              cellType = 'date';
            }
            // Проверяем, похоже ли значение на число
            else if (/^-?\d+(\.\d+)?$/.test(text)) {
              cellType = 'number';
            }
          }
          
          // Форматируем значение в соответствии с типом
          if (cellType) {
            formatCellValue(elementToFormat, cellType);
            processedCells++;
          }
        });
      });
      
      console.log(`Отформатировано ${processedCells} ячеек`);
      
      // Установка обработчика прокрутки для форматирования видимых строк
      if (rows.length > 50) {
        console.log('Установка отложенного форматирования для больших таблиц');
        
        // Форматируем остальные строки по мере прокрутки
        const handleScroll = debounce(() => {
          let moreProcessed = 0;
          
          rows.forEach((row, rowIndex) => {
            if (rowIndex <= 50) return; // Пропускаем уже обработанные
            
            // Проверяем, видима ли строка
            const rect = row.getBoundingClientRect();
            const isVisible = (
              rect.top >= 0 &&
              rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
            );
            
            if (isVisible) {
              const cells = row.querySelectorAll('td');
              
              cells.forEach((cell, cellIndex) => {
                const divWithData = cell.querySelector('div');
                const spanWithData = divWithData ? divWithData.querySelector('span') : null;
                const elementToFormat = spanWithData || divWithData || cell;
                
                if (!elementToFormat) return;
                
                // Если ячейка уже обработана, пропускаем
                if (elementToFormat.hasAttribute('data-formatted')) return;
                
                let cellType = cell.getAttribute('data-type');
                
                if (!cellType && columnTypes[cellIndex]) {
                  cellType = columnTypes[cellIndex];
                }
                
                if (!cellType) {
                  const text = elementToFormat.textContent.trim();
                  
                  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(text) || 
                      /^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}/.test(text) ||
                      /^\d{4}-\d{2}-\d{2}$/.test(text)) {
                    cellType = 'date';
                  }
                  else if (/^-?\d+(\.\d+)?$/.test(text)) {
                    cellType = 'number';
                  }
                }
                
                if (cellType) {
                  formatCellValue(elementToFormat, cellType);
                  moreProcessed++;
                }
                
                // Помечаем как обработанную
                elementToFormat.setAttribute('data-formatted', 'true');
              });
            }
          });
          
          if (moreProcessed > 0) {
            console.log(`Дополнительно отформатировано ${moreProcessed} ячеек при прокрутке`);
          }
        }, 200);
        
        // Добавляем обработчик прокрутки
        window.addEventListener('scroll', handleScroll);
      }
    } catch (error) {
      console.error('Ошибка при обработке таблицы:', error);
    }
  }
  
  /**
   * Форматирует значение ячейки по указанному типу
   * @param {HTMLElement} element - HTML-элемент для форматирования
   * @param {string} type - Тип данных ('date', 'number', etc.)
   */
  function formatCellValue(element, type) {
    const originalValue = element.textContent.trim();
    
    // Не форматируем пустые значения
    if (!originalValue) return;
    
    try {
      // Сохраняем оригинальное значение в атрибуте
      if (!element.hasAttribute('data-original-value')) {
        element.setAttribute('data-original-value', originalValue);
      }
      
      // Форматирование в зависимости от типа
      switch (type) {
        case 'date':
          const date = new Date(originalValue);
          if (!isNaN(date.getTime())) {
            // Форматирование даты
            if (originalValue.includes('T') || originalValue.includes(':')) {
              // Дата со временем
              element.textContent = date.toLocaleString('ru-RU');
            } else {
              // Только дата
              element.textContent = date.toLocaleDateString('ru-RU');
            }
          }
          break;
          
        case 'number':
          const num = parseFloat(originalValue);
          if (!isNaN(num)) {
            // Форматирование числа
            if (Number.isInteger(num)) {
              // Целое число
              element.textContent = num.toLocaleString('ru-RU');
            } else {
              // Число с десятичной частью
              element.textContent = num.toLocaleString('ru-RU', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              });
            }
          }
          break;
      }
    } catch (e) {
      console.error('Ошибка форматирования:', e);
    }
  }
  
  /**
   * Функция debounce для предотвращения частого вызова обработчика
   */
  function debounce(func, wait) {
    let timeout;
    return function() {
      const context = this, args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(context, args), wait);
    };
  }
  
  // Постоянная проверка наличия таблиц (для динамически загружаемых таблиц)
  function checkForTables() {
    // Проверяем наличие таблиц каждые 2 секунды, пока не найдем
    const checkInterval = setInterval(() => {
      if (tablesFound) {
        console.log('Таблицы уже найдены и обработаны, прекращаем проверку');
        clearInterval(checkInterval);
        return;
      }
      
      console.log('Проверка наличия таблиц...');
      const tables = document.querySelectorAll('table.min-w-full, table:not([class])');
      
      if (tables.length > 0) {
        console.log(`Найдено ${tables.length} таблиц после ожидания`);
        formatTableValues();
        clearInterval(checkInterval);
      }
    }, 2000);
    
    // Останавливаем проверку через 60 секунд в любом случае
    setTimeout(() => {
      if (!tablesFound) {
        console.log('Превышено время ожидания таблиц, прекращаем проверку');
        clearInterval(checkInterval);
      }
    }, 60000);
  }
  
  // Выполнить форматирование при загрузке страницы с небольшой задержкой
  function init() {
    console.log('Инициализация форматирования таблиц');
    
    // Первая попытка форматирования
    setTimeout(() => {
      formatTableValues();
      
      // Если таблицы не найдены, начинаем постоянную проверку
      if (!tablesFound) {
        console.log('Таблицы не найдены сразу, включаем режим постоянной проверки');
        checkForTables();
      }
    }, 1000);
  }
  
  // Подписываемся на событие загрузки страницы
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // Документ уже загружен, запускаем форматирование с задержкой
    init();
  }
  
  // Наблюдаем за изменениями в DOM с использованием debounce
  const observer = new MutationObserver(debounce(function(mutations) {
    // Если таблицы уже найдены, проверяем есть ли изменения в них
    if (tablesFound) {
      let tableChanged = false;
      
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
          // Проверяем, добавлены ли новые строки или ячейки в таблицу
          const addedNodes = Array.from(mutation.addedNodes);
          for (const node of addedNodes) {
            if (node.nodeType === 1) { // Элемент
              if (node.tagName === 'TR' || node.tagName === 'TD' || 
                  node.querySelector && node.querySelector('tr, td')) {
                tableChanged = true;
                break;
              }
            }
          }
        }
      });
      
      if (tableChanged) {
        console.log('Обнаружены изменения в таблице, запуск форматирования');
        formatTableValues();
      }
    } else {
      // Если таблицы еще не найдены, проверяем, не появились ли они
      let tableAdded = false;
      
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
          const addedNodes = Array.from(mutation.addedNodes);
          for (const node of addedNodes) {
            if (node.nodeType === 1) { // Элемент
              if (node.tagName === 'TABLE' || 
                  node.querySelector && node.querySelector('table')) {
                tableAdded = true;
                break;
              }
            }
          }
        }
      });
      
      if (tableAdded) {
        console.log('Обнаружено добавление таблицы в DOM, запуск форматирования');
        formatTableValues();
      }
    }
  }, 500));
  
  // Наблюдаем за изменениями в теле документа
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Добавляем информационное сообщение в консоль
  console.info('Форматирование таблиц активировано');
})(); 