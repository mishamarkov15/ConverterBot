from config import emoji


def get_support_text() -> list:
    text = [
        f"{emoji['outbox_tray']} Если Вы хотите сообщить об ошибке, предложить улучшения "
        f"или просто задать вопрос о работе бота,"
        f" можете обратиться к разработчику любым из ниже представленных методов."
    ]
    return text
