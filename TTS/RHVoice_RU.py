import speechd

tts = speechd.SSIPClient('test')
tts.set_output_module('rhvoice')
tts.set_language('ru')
tts.set_rate(30)
tts.set_punctuation(speechd.PunctuationMode.SOME)
tts.speak('И нежный вкус родимых слов так чисто губы холодит')
tts.close()
