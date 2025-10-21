import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm

BIELIK_MODEL_NAME = os.getenv("BIELIK_MODEL_NAME", "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0")

topic_identifier_agent = Agent(
    name="topic_identifier_agent",
    model=LiteLlm(model=f"ollama_chat/{BIELIK_MODEL_NAME}"),
    description=(
        """Agent odpowiedzialny za zidentyfikowanie tematu którym interesuje się użytkownik."""),
    instruction=("""
                Jesteś pomocnym agentem, który bazując *wyłącznie* na prośbie użytkownika,
                określi temat, którym użytkownik jest zainteresowany.
                Jeśli nie możesz zidentyfikować tematu, poproś użytkownika o jego podanie.
                Wspomnij o swojej zdolności do generowania krótkich artykułów na różnorodne tematy.
                """),
    output_key="user_topic",
)

topic_expander_agent = Agent(
    name="topic_expander_agent",
    model=LiteLlm(model=f"ollama_chat/{BIELIK_MODEL_NAME}"),
    description=(
        """Agent odpowiedzialny za rozwinięcie tematu którym interesuje się użytkownik.
        Generuje listę ciekawych faktów związanych z tematem."""),
    instruction=("""
                Twoim głównym zadaniem jest rozwinięcie tematu {user_topic} podanego
                przez użytkownika i utworzenie listy interesujących faktów, wykonując następujące 3 kroki:

                1. Przeprowadź dokładną analizę podanego tematu {user_topic} w celu zrozumienia jego istoty.
                2. Zidentifikuj najważniejsze aspekty lub kluczowe wnioski związane z tym tematem.
                3. Zsyntezuj najważniejsze aspekty i wnioski i przedstaw jako listę maksymalnie pięć faktów.
                 
                 """),
    output_key="initial_facts"
)

children_audience_agent = Agent(
    name="children_audience_agent",
    model=LiteLlm(model=f"ollama_chat/{BIELIK_MODEL_NAME}"),
    description=("""Agent odpowiedzialny za tworzenie treści skierowanych do dzieci."""),
    instruction=("""
                Jesteś super przyjaznym i pomysłowym Botem Wyjaśniającym!
                Twoim specjalnym zadaniem jest przekształcenie {initial_facts}
                w zabawne, łatwe do zrozumienia historie i wyjaśnienia dla 6-latka.
                Wyobraź sobie, że rozmawiasz z ciekawskim 6-latkiem, który uwielbia uczyć się nowych rzeczy.
                Twoje wyjaśnienia powinny być proste, angażujące i pełne kolorowych przykładów,
                aby pomóc małemu odkrywcy zrozumieć świat wokół niego
                """),
    output_key="children_article"
)

executive_audience_agent = Agent(
    name="executive_audience_agent",
    model=LiteLlm(model=f"ollama_chat/{BIELIK_MODEL_NAME}"),
    description=("""Agent odpowiedzialny za tworzenie treści skierowanych do kadry menedżerskiej.
                 (W oparciu o przekazaną listę faktów)"""),
    instruction=("""
                Jesteś ekspertem specjalizującym się w syntezie informacji w zwięzłe streszczenia.
                 Twoim zadaniem jest przekształcenie dostarczonej listy {initial_facts}
                 w przejrzysty, krótki raport, odpowiedni dla zapracowanego dyrektora lub osoby decyzyjnej.
                Końcowy raport powinien być bardzo krótki i zwięzły.
                """),
    output_key="executive_article"
)

authoring_agent = ParallelAgent(
    name="authoring_agent",
    description=("""Uruchamia w spósób równoległy pod-agentów odpowiedzialnych za tworzenie
                 treści dla różnych grup docelowych i platform."""),
    sub_agents=[children_audience_agent, executive_audience_agent]
)

content_creator_agent = SequentialAgent(
    name="content_creator_agent",
    description=(
        """Agent tworzący treści dla różnych grup docelowych i platform.
        Wykorzystuje pod-agentów do delegowania określonych zadań."""),
    sub_agents=[topic_identifier_agent, topic_expander_agent, authoring_agent]
)
root_agent = content_creator_agent
