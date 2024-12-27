from django_ai_assistant import AIAssistant, method_tool
from pydantic import BaseModel, Field
from search_app.models import CollectableShoe, ShoeDescription
from typing import Sequence
from langchain_core.tools import BaseTool
from langchain_community.retrievers import TFIDFRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
from langchain_core.documents import Document


# Structured Output for Shoe Recommendation Assistant
class AssistantResponse(BaseModel):
    """Response including conversational text and shoe component."""

    response: str = Field(description="A conversational response to the user's query")
    shoe_component: str = Field(
        description="the context for shoe recommendation",
    )


# AI Assistant: TOOL
class ShoeRecommendationAssistant(AIAssistant):
    """Assistant to answer questions related to collectable shoes in the database."""

    id = "shoe_recommendation_assistant"  # noqa: A003
    name = "Shoe Recommendation Assistant"
    instructions = (
        "You are an Assistant to support answering questions related to collectable shoes in your database. "
        "You must only provide recommendations based on the available shoes you have access to. "
        "You do not engage in conversations that are not related to your available shoes. "
        "Use the provided functions to answer queries and run operations.\n"
        "Maintain a friendly and casual tone. If no information is available for the user's questions, "
        "state that you don't have that specific detail. "
        "Your response must be in markdown syntax, here is an example: \n"
        "A conversational response to the user's query\n"
        "### {brand} {model} \n"
        "Color: {color}\n"
        "SKU: {sku_code}\n"
        "Rarity: {rarity}\n"
        "Collaboration Artist: {collaboration_artist}\n"
        "Year Produced: {year_produced}\n"
        "Retail Price: ${retail_price}\n"
        "Market Price: ${market_price}\n"
    )
    model = "gpt-4o-mini"
    tool_max_concurrency = 4
    structured_output = AssistantResponse

    def get_instructions(self):
        shoe_data_json = self.get_shoes()

        return "\n".join(
            [
                self.instructions,
                f"Available Shoes: {shoe_data_json}",
            ]
        )

    @method_tool()
    def get_shoes(self) -> str:
        """Get what shoes are in the database."""

        shoes = CollectableShoe.objects.all()  # pyright: ignore
        if not shoes:
            return "Empty"

        shoe_data_list = []
        for shoe in shoes:
            shoe_info = {
                "brand": shoe.brand,
                "model": shoe.model,
                "color": shoe.color,
                "sku_code": shoe.sku_code,
                "rarity": shoe.rarity,
                "collaboration_artist": shoe.collaboration_artist,
                "year_produced": shoe.year_produced,
                "retail_price": float(shoe.retail_price),
                "market_price": float(shoe.market_price),
                "quantity_on_release": shoe.quantity_on_release,
                "size": float(shoe.size),
            }
            shoe_data_list.append(shoe_info)

        return json.dumps(shoe_data_list)


# AI Assistant: RAG
class RAGShoeAssistant(AIAssistant):
    """Assistant to answer questions related to Shoes background using RAG over context stored in database."""

    id = "rag_shoe_assistant"  # noqa: A003
    name = "RAG Shoe Assistant"
    instructions = (
        "You are an assistant for answering questions related to the shoe's overiew. "
        "Use the following pieces of retrieved context from the shoe's documentation to answer "
        "the user's question. If you don't know the answer, state kindly that you don't "
        "know and recommend questions related to your knowledge. "
        "Use four sentences maximum and keep the answer concise."
    )
    model = "gpt-4o-mini"
    has_rag = True

    def get_instructions(self):
        return self.instructions

    def get_retriever(self) -> BaseRetriever:
        # NOTE: on a production application, you should persist or cache the retriever,
        # updating it only when documents change.
        docs = [
            Document(
                page_content=page.description,
                metadata={
                    "id": page.id,
                    "shoe": page.shoe.model if page.shoe else None,
                },
            )
            for page in ShoeDescription.objects.all()  # pyright: ignore
        ]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        retriever = TFIDFRetriever.from_documents(splits)
        return retriever


# AI Assistant: MAIN
class AISearchAssistant(AIAssistant):
    id = "ai_search_assistant"  # noqa: A003
    name = "AI Search Assistant"
    instructions = (
        "You are an AI Search Assistant responsible for assigning the user's query "
        "to the appropriate tools. For all questions related to shoe story and overview, use RAGShoeAssistant."
        "For all questions related to shoes inventory, price, model, brand and artist, use ShoeRecommendationAssistant. "
        "You do not directly engage in conversations with the user. "
        "Your response to the user are only generated from your tools with an exception "
        "for any questions not related to Shoe, you may then respond kindly "
        "that you don't know the answer and you able to answer questions related to available shoes. "
    )
    model = "gpt-4o-mini"

    def get_tools(self) -> Sequence[BaseTool]:
        return [
            ShoeRecommendationAssistant().as_tool(
                description="Tool to answer questions about specific details of "
                "shoes in the database, such as brand, model, "
                "price, and artist, year produced, quantity on release and more."
            ),
            RAGShoeAssistant().as_tool(
                description="Tool to provide background information and general "
                "knowledge about shoes including obverview, design, and more."
            ),
            *super().get_tools(),
        ]
