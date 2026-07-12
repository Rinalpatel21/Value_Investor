conversation = []


def add_message(role, content):

    conversation.append({

        "role": role,

        "content": content

    })


def get_messages():

    return conversation


def clear_messages():

    conversation.clear()