import gradio as gr
import re
import random
import time

class TextHumanizer:
    def __init__(self):
        self.contractions = {
            "do not": "don't", "does not": "doesn't", "did not": "didn't",
            "will not": "won't", "would not": "wouldn't", "should not": "shouldn't",
            "could not": "couldn't", "cannot": "can't", "are not": "aren't",
            "is not": "isn't", "was not": "wasn't", "were not": "weren't",
            "have not": "haven't", "has not": "hasn't", "had not": "hadn't",
            "I am": "I'm", "you are": "you're", "we are": "we're",
            "they are": "they're", "it is": "it's", "that is": "that's",
            "I will": "I'll", "you will": "you'll", "we will": "we'll",
            "they will": "they'll", "I have": "I've", "you have": "you've",
            "we have": "we've", "they have": "they've"
        }

        self.filler_words = ["well", "you know", "like", "um", "actually", "basically", "honestly"]
        self.transition_words = ["anyway", "so", "by the way", "speaking of which", "on that note"]

        self.formal_replacements = {
            "utilize": "use", "commence": "start", "terminate": "end",
            "implement": "do", "facilitate": "help", "obtain": "get",
            "demonstrate": "show", "indicate": "show", "provide": "give",
            "establish": "set up", "construct": "build", "generate": "create",
            "furthermore": "also", "therefore": "so", "consequently": "so",
            "subsequently": "then", "initially": "first", "ultimately": "finally"
        }

        self.sentence_starters = [
            "You know what?", "Here's the thing:", "Look,", "Listen,",
            "I mean,", "To be honest,", "Actually,", "Honestly,"
        ]

    def add_contractions(self, text):
        for formal, contraction in self.contractions.items():
            text = re.sub(r'\b' + re.escape(formal) + r'\b', contraction, text, flags=re.IGNORECASE)
        return text

    def add_filler_words(self, text, intensity=0.3):
        sentences = text.split('.')
        result = []
        for sentence in sentences:
            if sentence.strip():
                if random.random() < intensity:
                    filler = random.choice(self.filler_words)
                    if random.random() < 0.5:
                        sentence = filler + ", " + sentence.strip()
                    else:
                        words = sentence.split()
                        if len(words) > 3:
                            pos = random.randint(1, len(words) - 2)
                            words.insert(pos, filler + ",")
                            sentence = " ".join(words)
                result.append(sentence)
        return '.'.join(result)

    def vary_sentence_structure(self, text):
        sentences = text.split('.')
        result = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                if random.random() < 0.2:
                    starter = random.choice(self.sentence_starters)
                    sentence = starter + " " + sentence.strip()
                if i > 0 and random.random() < 0.15:
                    transition = random.choice(self.transition_words)
                    sentence = transition + ", " + sentence.strip()
                result.append(sentence)
        return '.'.join(result)

    def make_less_formal(self, text):
        for formal, casual in self.formal_replacements.items():
            text = re.sub(r'\b' + re.escape(formal) + r'\b', casual, text, flags=re.IGNORECASE)
        return text

    def add_personal_touches(self, text):
        personal_phrases = [
            "I think", "In my opinion", "From my experience", "I've found that",
            "Personally,", "I believe", "It seems to me", "I feel like"
        ]
        sentences = text.split('.')
        result = []
        for sentence in sentences:
            if sentence.strip():
                if random.random() < 0.3:
                    phrase = random.choice(personal_phrases)
                    sentence = phrase + " " + sentence.strip().lower()
                result.append(sentence)
        return '.'.join(result)

    def vary_punctuation(self, text):
        text = re.sub(r'\.(\s+)([A-Z])', r'...\1\2', text)
        sentences = text.split('.')
        result = []
        for sentence in sentences:
            if sentence.strip():
                if random.random() < 0.1:
                    sentence += "!"
                else:
                    sentence += "."
                result.append(sentence)
        return ''.join(result)

    def humanize_text(self, text, contractions, less_formal, filler_words, sentence_variety, personal_touches, punctuation_variety, filler_intensity):
        result = text
        if contractions:
            result = self.add_contractions(result)
        if less_formal:
            result = self.make_less_formal(result)
        if filler_words:
            result = self.add_filler_words(result, filler_intensity)
        if sentence_variety:
            result = self.vary_sentence_structure(result)
        if personal_touches:
            result = self.add_personal_touches(result)
        if punctuation_variety:
            result = self.vary_punctuation(result)
        return result

# Instance
humanizer = TextHumanizer()

# Gradio UI
def gradio_interface(text, contractions, less_formal, filler_words, sentence_variety, personal_touches, punctuation_variety, filler_intensity):
    return humanizer.humanize_text(
        text,
        contractions,
        less_formal,
        filler_words,
        sentence_variety,
        personal_touches,
        punctuation_variety,
        filler_intensity
    )

demo = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Input Text", lines=7, placeholder="Paste your AI-generated text here..."),
        gr.Checkbox(label="Add Contractions", value=True),
        gr.Checkbox(label="Make Less Formal", value=True),
        gr.Checkbox(label="Add Filler Words", value=True),
        gr.Checkbox(label="Vary Sentence Structure", value=True),
        gr.Checkbox(label="Add Personal Touches", value=True),
        gr.Checkbox(label="Vary Punctuation", value=True),
        gr.Slider(minimum=0.1, maximum=0.7, step=0.1, value=0.3, label="Filler Intensity")
    ],
    outputs=gr.Textbox(label="Humanized Output"),
    title="Shaurya - Make AI Text Sound Natural",
    description="Turn robotic-sounding AI text into something more natural, casual, and personal."
)

demo.launch()
