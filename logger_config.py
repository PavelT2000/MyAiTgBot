"""
Start configuration of logger
"""
import logging
import os

def setup_logging():
    """
    Настройка логов
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("📁 Папка 'logs' создана автоматически")
    # Базовый формат записи
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 1. Логгер для БД
    db_handler = logging.FileHandler('logs/database.log', encoding='utf-8')
    db_handler.setFormatter(formatter)
    db_logger = logging.getLogger('database')
    db_logger.addHandler(db_handler)
    db_logger.setLevel(logging.INFO)
    # 2. Логгер для прокси
    proxy_handler = logging.FileHandler('logs/proxy.log', encoding='utf-8')
    proxy_handler.setFormatter(formatter)
    proxy_logger = logging.getLogger('proxy')
    proxy_logger.addHandler(proxy_handler)
    proxy_logger.setLevel(logging.INFO)
    # 3. Логгер для сервиса
    service_handler = logging.FileHandler('logs/service.log', encoding='utf-8')
    service_handler.setFormatter(formatter)
    service_logger = logging.getLogger('service')
    service_logger.addHandler(service_handler)
    service_logger.setLevel(logging.INFO)
    # 4. Логгер для Ошибок (только ERROR и выше)
    error_handler = logging.FileHandler('logs/errors.log', encoding='utf-8')
    error_handler.setFormatter(formatter)
    error_logger = logging.getLogger('errors')
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)
    # 5. Вывод в консоль (чтобы видеть всё сразу)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler) # Корневой логгер
    logging.getLogger().setLevel(logging.INFO)
