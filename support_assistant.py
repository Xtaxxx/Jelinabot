# support_assistant.py
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, QueryBundle, get_response_synthesizer,PromptTemplate,SimpleDirectoryReader
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SentenceSplitter
from config import Config
from llm import LLMInitializer
from llama_index.core.response_synthesizers import ResponseMode


class SupportAssistant:
    def __init__(self):
        self.query_wrapper_prompt = PromptTemplate(
            "[INST]<<SYS>>\n" + Config.SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
        )
        self.qa_prompt_tmpl = PromptTemplate(Config.qa_prompt_tmpl_str)
        self.refine_prompt_tmpl = PromptTemplate(Config.refine_prompt_tmpl_str)
        self._initialize_logging()
        self.llm = LLMInitializer.initialize_llm()
        if(Config.EMB_CONFIG):
            # 读取文档
            documents = SimpleDirectoryReader(Config.INDEX_DATAS).load_data()
            # 对文档进行切分，将切分后的片段转化为embedding向量，构建向量索引
            index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=256)])
            # 将embedding向量和向量索引存储到文件中
            index.storage_context.persist(persist_dir=Config.PERSIST_DIR)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=Config.PERSIST_DIR)
            index = load_index_from_storage(storage_context)
        self.retriever = VectorIndexRetriever(
                            index=index,
                            similarity_top_k=5)
        self.response_synthesizer = get_response_synthesizer(
                            response_mode=ResponseMode.REFINE)
        self.query_engine = RetrieverQueryEngine(retriever=self.retriever,
                            response_synthesizer=self.response_synthesizer)#node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.6)],

    def _initialize_logging(self):
        from logging_config import setup_logging
        setup_logging()

    def retrieve_contexts(self, query):
        contexts = self.query_engine.retrieve(QueryBundle(query))
        return contexts

    def query(self, query):
        # 更新查询引擎中的prompt template
        self.query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": self.qa_prompt_tmpl,
        "response_synthesizer:refine_template": self.refine_prompt_tmpl})
        response = self.query_engine.query(query)
        return response