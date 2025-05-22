from openai import OpenAI

client = OpenAI(
    base_url="https://chat38.com/v1",
    api_key="sk-cbqb7AsEZdpSUTfEKyD4nKa3YLJfb8CjNH4dn3asne8gpzU9"
)

completion = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=16384,
    messages=[
        {"role": "user", "content": "hi"}
    ]
)
print(completion)