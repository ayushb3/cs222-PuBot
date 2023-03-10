import sys
import os
sys.path.append(os.getcwd() + '/src/')
from title_generator import generate_title

def test_title_generator():
    text = """Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.
                Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.
                Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0. Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2.
                Python consistently ranks as one of the most popular programming languages."""
    have = generate_title(text)
    print(have)
    assert 0 < len(have) < len(text)

if __name__ == '__main__':
    test_title_generator()