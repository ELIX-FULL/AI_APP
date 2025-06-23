# services/image_generator.py
import asyncio
import base64
import json
import logging
import aiohttp


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    # ИЗМЕНЕНИЕ 1: Новый метод и эндпоинт для получения pipeline
    async def get_pipeline(self):
        """Получает ID доступного пайплайна."""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS) as response:
                if response.status != 200:
                    logging.error(f"Error getting pipeline. Status: {response.status}. Text: {await response.text()}")
                    return None

                data = await response.json()
                if not data:
                    logging.error("No pipelines found in the API response.")
                    return None

                # Возвращаем ID первого доступного пайплайна
                return data[0].get('id')

    # ИЗМЕНЕНИЕ 2: Новый метод generate, эндпоинт и параметры
    async def generate(self, prompt: str, pipeline_id: int, images: int = 1, width: int = 1024,
                       height: int = 1024) -> str | None:
        """Запускает генерацию изображения через pipeline."""
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        # Используем FormData для отправки файлов и параметров
        data = aiohttp.FormData()
        data.add_field('pipeline_id', str(pipeline_id))
        data.add_field('params', json.dumps(params), content_type='application/json')

        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS,
                                    data=data) as response:
                if response.status != 201:
                    logging.error(
                        f"Error starting generation via pipeline. Status: {response.status}. Text: {await response.text()}")
                    return None

                data = await response.json()
                return data.get('uuid')

    # ИЗМЕНЕНИЕ 3: Новый эндпоинт и структура ответа в check_generation
    async def check_generation(self, request_id: str, attempts: int = 10, delay: int = 10) -> bytes | None:
        """Проверяет статус генерации в пайплайне."""
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.URL + 'key/api/v1/pipeline/status/' + request_id,
                                       headers=self.AUTH_HEADERS) as response:
                    if response.status != 200:
                        logging.error(
                            f"Error checking pipeline status. Status: {response.status}. Text: {await response.text()}")
                        return None

                    data = await response.json()
                    if data.get('status') == 'DONE':
                        # В новой версии API результат лежит в 'result' -> 'files'
                        files = data.get('result', {}).get('files', [])
                        if files:
                            # Декодируем первое изображение из base64
                            image_base64 = files[0]
                            return base64.b64decode(image_base64)
                    elif data.get('status') == 'FAIL':
                        logging.error(f"Image generation failed on server (pipeline): {data}")
                        return None

            attempts -= 1
            await asyncio.sleep(delay)

        logging.warning("Generation timeout. The image was not ready in time.")
        return None