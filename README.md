# r1-lmstudio-chat

> A simple deepseek r1 based chatbot made with Streamlit and lmstudio backend

## llm backend

LM Studio Rest API. Download LM Studio, then load `deepseek-r1-distill-qwen-7b` and start the server.

## running locally

> [!IMPORTANT]
> Make sure to start the llm backend first!

Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once installed,

```bash
git clone https://github.com/ShawonAshraf/r1-lmstudio-chat.git
cd r1-lmstudio-chat
uv venv
source .venv/bin/activate
uv pip install -e .
```

Now you can run the chatbot

```bash
uv run streamlit run bot.py
```

## disclaimer

This isn't a production ready chatbot and is only meant to be used as a demo.
