# Eskadra Bielik - Misja 1
Przykładowy kod źródłowy pozwalający na:

* Skonfigurowanie własnej instancji modelu [Bielik](https://ollama.com/SpeakLeash/bielik-4.5b-v3.0-instruct) w oparciu o [Ollama](https://ollama.com/)
* Skonfigurowanie prostych systemów agentowych przy wykorzystaniu [Agent Development Kit](https://google.github.io/adk-docs/)
* Uruchomienie obu powyższych serwisów na [Cloud Run](https://cloud.google.com/run?hl=en)

## Instrukcja

### Wymagania

*   Komputer z dostępem do internetu
*   Nowoczesna przeglądarka
*   Konto Google (np. @gmail.com)

### Kroki

1. Uzyskaj kredyt Cloud **OnRamp**, lub skonfiguruj płatności w projekcie Google Cloud
2. Przejdź do **Google Cloud Console**: [console.cloud.google.com](https://console.cloud.google.com)
3. Stwórz nowy projekt Google Cloud i wybierz go aby był aktywny
4. Otwórz Cloud Shell ([dokumentacja](https://cloud.google.com/shell/docs))
5. Sklonuj repozytorium z przykładowym kodem i przejdź do nowoutworzonego katalogu

   ```bash
   git clone https://github.com/avedave/eskadra-bielik-misja1
   cd eskadra-bielik-misja1
   ```
6. Stwórz i aktywuj wirtualne środowisko Python
   
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
   *   Skopiuj zawartość pliku `.env.sample` do nowego pliku `.env`
   	```bash
   	cp .env.sample .env
   	```
   *   Dodaj wartość klucza ze swojego Gemini API key jako wartość zmiennej `GOOGLE_API_KEY` w pliku `.env`
9. Uruchom agenta w konsoli **Cloud Shell**:
	
   ```bash
	 adk run content_creator
	```
10.  Przetestuj agenta w środowisku Web
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