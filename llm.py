# llm.py
import torch
import logging
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.core import Settings,PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import Config


query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + Config.SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)
qa_prompt_tmpl = PromptTemplate(Config.qa_prompt_tmpl_str)
refine_prompt_tmpl = PromptTemplate(Config.refine_prompt_tmpl_str)

class LLMInitializer:
    @staticmethod
    def initialize_llm():
        try:
            llm = HuggingFaceLLM(
                context_window=4096,
                max_new_tokens=2048,
                generate_kwargs={"temperature": 0.2, "do_sample": False},
                query_wrapper_prompt=query_wrapper_prompt,
                tokenizer_name=Config.TOKENIZER_NAME,
                model_name=Config.MODEL_NAME,
                device_map="auto",
                model_kwargs={"torch_dtype": torch.float32},
            )
            Settings.llm = llm

            llama_debug = LlamaDebugHandler(print_trace_on_end=True)
            callback_manager = CallbackManager([llama_debug])
            Settings.callback_manager = callback_manager

            Settings.embed_model = HuggingFaceEmbedding(model_name=Config.EMBED_MODEL_NAME)
            return llm
        except Exception as e:
            logging.error(f"Failed to initialize LLM: {e}")
            raise