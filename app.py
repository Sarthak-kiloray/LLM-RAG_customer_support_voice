import tempfile
import base64

import gradio as gr
from gradio.blocks import Blocks

from rag_chain import get_rag_chain
from tts_agent import synthesize_speech, OPENAI_TTS_VOICES



def _patched_get_api_info(self):
 
    return {
        "named_endpoints": {},
        "unnamed_endpoints": [],
        "dependencies": [],
    }


Blocks.get_api_info = _patched_get_api_info



rag_chain = get_rag_chain()


def answer_and_speak(question: str, voice: str):
    """Handle a single user query: RAG -> TTS."""

    question = (question or "").strip()
    if not question:
        return "Please enter a question.", "No context documents.", None, ""

    # 1) RAG: get answer + context
    result = rag_chain.invoke({"input": question})
    answer = result.get("answer", "").strip()
    context_docs = result.get("context", [])

    # Build a human-readable context snippet
    context_snippets = []
    for i, doc in enumerate(context_docs[:3]):
        metadata = getattr(doc, "metadata", {}) or {}
        source = metadata.get("source", "unknown")
        snippet = (doc.page_content or "").replace("\n", " ")[:400]
        context_snippets.append(f"Source {i+1} ({source}):\n{snippet}...")
    context_text = "\n\n".join(context_snippets) if context_snippets else "No context documents."

    # 2) TTS
    audio_bytes = synthesize_speech(answer, voice=voice)

    # Save audio to temp file for Gradio playback
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    with open(tmp.name, "wb") as f:
        f.write(audio_bytes)
    audio_path = tmp.name

    # Build download link
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    download_link = f'<a href="data:audio/mpeg;base64,{audio_b64}" download="response.mp3">Download audio</a>'

    return answer, context_text, audio_path, download_link


with gr.Blocks() as demo:
    gr.Markdown("# 📞 Customer Support Voice Agent\nAsk a question and get a spoken answer from your docs.")

    with gr.Row():
        with gr.Column(scale=3):
            question = gr.Textbox(
                label="Your question",
                placeholder="Ask something about the product or docs...",
                lines=3,
            )
            voice = gr.Dropdown(
                choices=OPENAI_TTS_VOICES,
                value="nova",
                label="Voice",
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column(scale=4):
            answer_box = gr.Textbox(
                label="Answer",
                lines=5,
                interactive=False,
            )
            context_box = gr.Textbox(
                label="Retrieved context (debug / transparency)",
                lines=6,
                interactive=False,
            )
            audio_out = gr.Audio(
                label="Audio Response",
                type="filepath",
            )
            download_html = gr.HTML(value="")


    ask_btn.click(
        fn=answer_and_speak,
        inputs=[question, voice],
        outputs=[answer_box, context_box, audio_out, download_html],
    )


if __name__ == "__main__":
    demo.launch(
        show_api=False,  
        debug=True,
    )
