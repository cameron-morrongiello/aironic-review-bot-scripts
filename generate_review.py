import openai
import os

if not os.getenv('GITHUB_ACTIONS'):
    # Code is running locally
    from dotenv import load_dotenv
    load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_sarcastic_review(product_title, product_description):
    prompt = f"Create a short, funny, dark humor and saracstic product review of the following product and description for a Twitter post. Incude some hastags.\nProduct: {product_title}\nDescription: {product_description}"
    model = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a sarcastic, funny, dark humor, and whitty influencer. Respond in 3 sentences MAX."},
            {"role": "user", "content": prompt},
        ]
    )

    return __clean_review(response.choices[0].message.content)


def __clean_review(review):
    cleand_review = __remove_surrounding_quotations(review)
    return cleand_review


def __remove_surrounding_quotations(string: str):
    if string.startswith('"'):
        string2 = string.replace('"', '', 1)
        return __replace_last(string2, '"', '')
    else:
        return string


def __replace_last(source_string, replace_what, replace_with):
    # https://stackoverflow.com/questions/3675318/how-to-replace-some-characters-from-the-end-of-a-string

    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail
