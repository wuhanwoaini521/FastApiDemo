
class openText:

    def __init__(self, filename, mode):
        self.wr = open(filename, mode)

    def __enter__(self):
        return self.wr

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wr.close()

with openText('text.txt', 'a') as f:
    f.write('hello world!')
