import wikipedia
wikipedia.set_lang("en")
try:
    page = wikipedia.page("Arthur Morgan (Red Dead)")
    images = [img for img in page.images if img.endswith(('.jpg', '.png'))]
    if images:
        print("Success:", images[0])
    else:
        print("No image")
except Exception as e:
    print("Error:", e)
