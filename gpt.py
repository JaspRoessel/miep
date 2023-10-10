import os
impott openai
import tiktoken
from key import OPEN_API_KEY

# Copied with minor changes from: https://platform.openai.com/docs/guides/chat/managing-tokens and the youtube channel DougDoug
def num_tokens_from_messages(messages, model='gpt-3.5-turbo'):
    """Returns the number of tokens used by a list of messages"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
         encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

class GptManager:
    chat_history = []

    def __init__(self) -> None:
        open_api_key = OPEN_API_KEY
    
    def chat(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return
        
        print("\nAsking ChatGPT a question...")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [{"role": "user", "content": prompt}],
            temperature= 1.2
        )
        print("we got an answer! \n")
        user = completion.choices[0].message.role
        answer = completion.choices[0].message.content
        print(f"Here was the user {user}")
        print(f"Here was the answer {answer}")
        return answer

    def chat_with_history(self, prompt="") -> None:
        if not prompt:
            print("Didn't receive input!")
            return
        
        #Add prompt into chat history
        self.chat_history.append({"role": "user", "content": prompt})

        #Check total token limit. Remove old messages if needed
        print(f"Chat history has current token length of {num_tokens_from_messages(self.chat_history)}")
        while num_tokens_from_messages(self.chat_history) > 3200:
            self.chat_history.pop(1)
            self.chat_history.pop(1)
            print(f"Popped a message! New token length is: {num_tokens_from_messages(self.chat_history)}")
        
        print("\nAsking ChatGPT a question...")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            temperature= 1.2
        )
        print("we got an answer! \n")

        answer = completion.choices[0].message.content

        #Add this answer to our chat history
        self.chat_history.append({"role": completion.choices[0].message.role, "content": answer})

        print(answer)
        return answer

if __name__ is '__main__':
    gm = GptManager()

    FIRST_SYSTEM_MESSAGE = {"role": "system", "content": "aaaaaaaaaaaaa"}
    FIRST_USER_MESSAGE = {"role": "user", "content": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    gm.chat_history.append(FIRST_SYSTEM_MESSAGE)
    gm.chat_history.append(FIRST_USER_MESSAGE)

    while True:
        new_prompt = input("\nPlease enter prompt \n\n")
        gm.chat_with_history(new_prompt)