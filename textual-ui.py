from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, RadioSet, RadioButton, ProgressBar, RichLog, Label, Static, TextArea
from textual.containers import Horizontal, Vertical


class ApiAssistApp(App):

    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        # Header and Footer
        yield Header()
        yield Footer()

        # Main layout
        with Horizontal():

            # Left side - inputs and radio buttons
            with Vertical():
                yield Label("ChromaDB Directory")
                yield Input(placeholder="Enter ChromaDB directory", id="db_directory")

                yield Label("Collection Name")
                yield Input(placeholder="Enter collection name", id="collection_name")

                yield Label("Embedding Model")
                yield Input(placeholder="Enter embedding model", id="embedding_model")

                yield Label("Chat Model")
                yield Input(placeholder="Enter chat model", id="chat_model")

                with Horizontal():
                    yield Label("Choose Embedding Type")
                    with RadioSet(id="embedding_type"):
                        yield RadioButton("Ollama", id="embedding_ollama")
                        yield RadioButton("Hugging Face", id="embedding_huggingface")

                    yield Label("Choose Language Model Type")
                    with RadioSet(id="language_model_type"):
                        yield RadioButton("Ollama", id="llm_ollama")
                        yield RadioButton("Hugging Face", id="llm_huggingface")  

                with Vertical():    
                    yield Label("Enter your message:")
                    yield TextArea(id="chat_input")
                    yield Button(label="Send", id="send_button")  # Add a Send button     

            # Right side - progress and log
            with Vertical():
                with Horizontal():    
                    yield Button(label="Start", id="start_button")
                    yield Button(label="Stop", id="stop_button", disabled=True)   
                    yield ProgressBar(id="progress_bar")
                yield Label("Chat Log")
                yield RichLog(id="log_widget", auto_scroll=True)
                status_widget = Static(id="status")
                status_widget.update("Status: Ready")
                yield status_widget
         
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_button":
            await self.start_process()
        elif event.button.id == "stop_button":
            await self.stop_process()
        elif event.button.id == "send_button":  # Handle the send button press
            await self.send_message()

    async def send_message(self):
        """Handles sending the message from the chat input."""
        chat_input = self.query_one("#chat_input", TextArea)
        message = chat_input.text.strip()

        if message:
            # Log the message to the chat log
            self.log_message(f"User: {message}")
            chat_input.text = ""  # Clear the input after sending the message

    async def start_process(self):
        status_widget = self.query_one("#status")
        status_widget.update("Status: Starting...")
        # Logic for starting the process, loading database, etc.
        # Update progress and logs

    async def stop_process(self):
        status_widget = self.query_one("#status")
        status_widget.update("Status: Stopping...")
        # Logic for canceling the process

    def log_message(self, message: str):
        """Helper function to log messages to the RichLog widget."""
        self.query_one("#log_widget").write(message)

    def update_progress(self, progress: int):
        """Helper function to update the progress bar."""
        self.query_one("#progress_bar").update(progress)


if __name__ == "__main__":
    app = ApiAssistApp()
    app.run()
