# Eskadra Bielik - Misja 1
Przykładowy kod źródłowy pozwalający na:

* Skonfigurowanie własnej instancji modelu [Bielik](https://ollama.com/SpeakLeash/bielik-4.5b-v3.0-instruct) w oparciu o [Ollama](https://ollama.com/)
* Skonfigurowanie prostych systemów agentowych przy wykorzystaniu [Agent Development Kit](https://google.github.io/adk-docs/)
* Uruchomienie obu powyższych serwisów na [Cloud Run](https://cloud.google.com/run?hl=en)

## Przygotowanie projektu Google Cloud

1. Uzyskaj kredyt Cloud **OnRamp**, lub skonfiguruj płatności w projekcie Google Cloud
2. Przejdź do **Google Cloud Console**: [console.cloud.google.com](https://console.cloud.google.com)
3. Stwórz nowy projekt Google Cloud i wybierz go aby był aktywny
4. Otwórz Cloud Shell ([dokumentacja](https://cloud.google.com/shell/docs))
5. Sklonuj repozytorium z przykładowym kodem i przejdź do nowoutworzonego katalogu
   ```bash
   git clone https://github.com/avedave/eskadra-bielik-misja1
   cd eskadra-bielik-misja1
   ```
6. Zmień nazwę pliku `.env.sample` na `.env`
   ```bash
   mv .env.sample .env
   ```
7. Zaktualizuj potrzebne zmienne środowiskowe w pliku `.env`
   Na tym etapie `.env` zawiera: zmienną definiującą region Google Cloud
   `GOOGLE_CLOUD_LOCATION`, domyślną nazwę dla usługi gdzie uruchomimy Bielika `BIELIK_SERVICE_NAME` oraz wersję Bielika z której będziemy korzystać `BIELIK_MODEL_NAME`
   
   ```bash
   GOOGLE_CLOUD_LOCATION="europe-west1"  # Europe (Belgium)
   BIELIK_SERVICE_NAME="ollama-bielik-v3"
   BIELIK_MODEL_NAME="SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"
   ```
   >[!IMPORTANT]
   >Jeżeli zmieniasz w `BIELIK_MODEL_NAME` domyślny model Bielika na inną wersję, to zaktualizuj tę informację również w pliku Dockerfile:
   
   ```dockerfile
   ENV MODEL SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0
   ```
   
   Wczytaj zmienne środowiskowe korzystając z podręcznego skryptu
   
   ```bash
   source reload-env.sh
   ```
## Własna instancja Bielika

```bash
gcloud run deploy $BIELIK_SERVICE_NAME --source ollama-bielik/ --region $GOOGLE_CLOUD_LOCATION --concurrency 7 --cpu 8 --set-env-vars OLLAMA_NUM_PARALLEL=4 --gpu 1 --gpu-type nvidia-l4 --max-instances 1 --memory 16Gi --allow-unauthenticated --no-cpu-throttling --no-gpu-zonal-redundancy --timeout 600 --labels dev-tutorial=codelab-dos-bielik
```
### Jak sprawdzić, czy usługa działa?
* Sprawdź w Google  Cloud console czy nowy serwis jest już dostępny
* Sprawdź czy otwierając URL w przeglądarce zobaczysz informację: `Ollama is running`
* Sprawdź przez API jakie modele są dostępne lokalnie na serwerze Ollama
   ```bash
   curl "${OLLAMA_URL}/api/tags"
   ```
* Wyślij zapytanie przez API
   ```bash
   curl "${OLLAMA_URL}/api/generate" -d "{
      \"model\": \"$BIELIK_MODEL_NAME\",
      \"prompt\": \"Kto zabił smoka wawelskiego?\",
      \"stream\": false
   }"
   ```

## Pierwszy agent

1. Przejdź do katalogu z agentami

   ```bash
   cd adk-agents
   ```
2. Stwórz i aktywuj wirtualne środowisko Python

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
7. Zainstaluj wymagane komponenty

   ```bash
   pip install -r requirements.txt
   ```
8. Skonfiguruj swój własny klucz Gemini API
   *   Stwórz lub skopiuj istniejący Gemini API key z [Google AI Studio](https://ai.dev).
   *   Dodaj wartość klucza ze swojego Gemini API key jako wartość zmiennej `GOOGLE_API_KEY` w pliku `.env`
9. Uruchom agenta w konsoli **Cloud Shell**:

   ```bash
    adk run content_creator
   ```
10. Przetestuj agenta w środowisku Web
    1. Uruchom środowisko ADK Web
    ```bash
    adk web
    ```
    2. Zmień port w **Web View** (jeżeli potrzeba, zazwyczaj jest to port 8000)
    3. Zaakceptuj zmiany poprzez: *Change and Preview*

11. Deploy to Cloud Run:
    ```bash
    gcloud run deploy multi-tool-agent --source . --region europe-west1 --allow-unauthenticated --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=FALSE, GOOGLE_API_KEY="  --labels dev-tutorial=codelab-dos
    ```

Deployment documentation: https://google.github.io/adk-docs/deploy/cloud-run/#python---gcloud-cli