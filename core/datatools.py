import json
import logging
import os
import ssl
from contextlib import contextmanager
from urllib import error, request, parse
from tempfile import NamedTemporaryFile
from typing import Optional, Iterator

from core import consts

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Базовый клиент для отправки запросов во внешний сервис по стандарту "jsonrpc 2.0".
    :param url: Базовый url-адрес внешнего сервиса
    :type url: str
    """

    def __init__(self, url: str) -> None:
        self._url = url

    def request(
            self,
            endpoint: str,
            method: str,
            params: Optional[dict] = None,
            client_id: Optional[int] = None,
    ) -> dict:
        """
        Метод отправки запроса.
        :param endpoint: Конечная точка url внешнего сервиса
        :type endpoint: str
        :param method: Имя вызываемого метода
        :type method: str
        :param params: Данные, которые должны быть переданы методу, как параметры
        :type params: dict, optional
        :param client_id: Идентификатор для установки соответствия между запросом и ответом
        :type client_id: int, optional
        :return: Данные с внешнего сервиса
        :rtype: dict
        """
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        with (self.create_temp_file(data=consts.CERT) as cert_file,
              self.create_temp_file(data=consts.KEY) as key_file):
            context.load_cert_chain(certfile=cert_file.name, keyfile=key_file.name)

            context.set_ciphers('HIGH:!DH:!aNULL')
            context.verify_mode = ssl.CERT_OPTIONAL

            payload = {
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': client_id,
            }
            payload = json.dumps(payload).encode('utf-8')
            request_data = {
                'url': parse.urljoin(self._url, endpoint),
                'data': payload,
                'headers': {'Content-Type': 'application/json'},
            }
            try:
                with request.urlopen(request.Request(**request_data), context=context) as response:
                    return json.loads(response.read().decode('utf-8'))
            except (error.HTTPError, ssl.SSLError) as e:
                logger.error(f'During request error occurred: {e}')
                return {'error': e}
            except Exception as e:
                logger.error(f'Unhandled exception: {e}')
                return {'error': e}

    @contextmanager
    def create_temp_file(self, data: str) -> Iterator[NamedTemporaryFile]:
        """
        Метод для получения временного файла с данными.
        :param data: Данные для записи во временный файл
        :type data: str
        :return: Временный файл с записанными данными
        :rtype: NamedTemporaryFile
        """
        temp_file = NamedTemporaryFile(delete=False)
        try:
            temp_file.write(data.encode('utf-8'))
            temp_file.close()
            yield temp_file
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)


class Client(BaseClient):
    def __init__(self, url: str = 'https://slb.medv.ru/') -> None:
        super().__init__(url=url)
