import json

class RequestBot:
    """Класс, отвечающий за работу бота, подающего предложения через запросы, а не через интерфейс."""
    def get_cookies(self, driver):
        """
        Получает куки.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Объект с куки
        """
        cookies = list(driver.get_cookies())
        cookie_objects = []

        for cookie in cookies:
            cookie_object = {
                "Name": cookie["name"],

                "Value": cookie["value"]
            }

            cookie_objects.append(cookie_object)

        return cookie_objects

    def get_local_storage(self, driver):
        """
        Получить значения из локального хранилища.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Объект со значениями локального хранилища.
        """
        script = """
                var items = {};
                for (var i = 0; i < localStorage.length; i++){
                    var key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
                """
        local_storage_items = driver.execute_script(script)

        return local_storage_items

    def get_access_token(self, local_storage_items):
        """
        Получает токен доступа.
        :param local_storage_items: Объект со всеми значениями локального хранилища
        :return: Токен доступа.
        """
        authorization_data = local_storage_items['0-eat_ui']
        authorization_data_dict = json.loads(authorization_data)
        authn_result = authorization_data_dict['authnResult']
        token_access = authn_result['access_token']

        return token_access

    def get_cart_id(self, local_storage_items):
        cart_id = local_storage_items['cart_id']

        return cart_id