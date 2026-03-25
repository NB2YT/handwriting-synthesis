from demo import Hand
import numpy as np
import textwrap

if __name__ == "__main__":
    hand = Hand()

    text = "Canada is considered one of the best countries in the world to live in. First, Canada has an excellent health care system, allowing all citizens access to medical services at a reasonable price. Second, Canada has a high standard of education, with students taught by well-trained teachers who encourage university studies. Finally, Canada's cities are clean and efficiently managed, offering many parks and ample space for residents. As a result, Canada is a highly desirable place to live."

    lines = textwrap.wrap(text, width=30)
    #max = 2.5 min=0.15
    biases = [0.75 for i in lines]
    #0-12
    styles = [7 for i in lines]

    hand.write(
        filename='img/test.svg',
        lines=lines,
        biases=biases,
        styles=styles,
    )
